import multiprocessing
import time
import signal
import os
import threading # Ensure this import is present

# Importations relative to your qtask_py package
from . import config
from .worker import start_worker_process # start_worker_process will also need an update
from .qtask import qtask, NoHandlerRegisteredError


class StreamOrchestrator:
    def __init__(self, num_workers_per_partition: int = 1, handler_modules: list[str] | None = None): # MODIFIED
        if num_workers_per_partition != 1:
            print(
                "Warning: This example is simplified for 1 worker per partition.",
                flush=True
            )
            print(
                "For multiple pods competing, the generated consumer_id MUST be globally unique.",
                flush=True
            )

        self.num_partitions = config.NUMBER_OF_PARTITIONS
        self.processes = []
        self._shutdown_flag = multiprocessing.Event()
        self.pod_identifier = os.getenv("POD_NAME", f"pod-{os.getpid()}-{threading.get_ident()}")
        
        self.handler_modules = handler_modules if handler_modules is not None else [] # MODIFIED: Store handler modules

        if not qtask.is_any_handler_registered() and not self.handler_modules:
            # If no handlers are registered at orchestrator init AND no handler modules are provided
            # for workers to load, then it's likely a configuration issue.
            # Note: qtask.is_any_handler_registered() here checks the main process's qtask instance.
            # Workers will register their own. This check is more of a safeguard.
            print(
                f"Warning for Orchestrator ({self.pod_identifier}): No handlers seem to be registered globally "
                "at orchestrator initialization, and no specific handler_modules were provided for workers. "
                "Ensure handlers are defined in modules passed to 'handler_modules' or are globally discoverable by workers.",
                flush=True
            )
        elif not self.handler_modules and qtask.is_any_handler_registered():
             print(
                f"Warning for Orchestrator ({self.pod_identifier}): Handlers are registered in the main process, "
                "but no 'handler_modules' were specified for workers. Workers might not find these handlers "
                "unless the modules are re-imported within each worker.",
                flush=True
            )


        # Initial validation in the main process (qtask.is_any_handler_registered() checks the current process's qtask instance)
        # This doesn't guarantee workers will find them unless handler_modules are used.
        if not qtask.is_any_handler_registered():
             # This check might be too strict if all handlers are meant to be loaded by workers via handler_modules
             # For now, we keep it as it was, but it implies handlers should be discoverable by the main process too.
            critical_error_message = (
                f"CRITICAL ERROR when starting Orchestrator ({self.pod_identifier}): No message handler has been registered "
                "in the main process.\nEnsure that you have defined at least one function with the @qtask.handler decorator "
                "or provide 'handler_modules' to the StreamOrchestrator."
            )
            # print(critical_error_message, flush=True) # Commenting out to avoid premature exit if relying on worker loading
            # raise NoHandlerRegisteredError("No topic handler has been registered in the system (main process).")
            print(f"Orchestrator ({self.pod_identifier}): No handlers registered in the main process's qtask instance. "
                  "Relying on workers to load handlers from specified 'handler_modules'.", flush=True)
        else:
            print(f"Orchestrator ({self.pod_identifier}): Handlers are registered in the main process's qtask instance. "
                  "Ensure these are also accessible or re-registered in workers via 'handler_modules'.", flush=True)

            
    def _handle_orchestrator_signal(self, signum, frame):
        print(
            f"Orchestrator ({self.pod_identifier}): Signal {signum} received directly by orchestrator. Starting shutdown...",
            flush=True
        )
        self._shutdown_flag.set()

    def start(self):
        print(
            f"Orchestrator ({self.pod_identifier}) starting {self.num_partitions} workers...",
            flush=True
        )

        if threading.current_thread() is threading.main_thread():
            print(f"Orchestrator ({self.pod_identifier}): Running in main thread. Registering signal handlers for SIGINT and SIGTERM.", flush=True)
            try:
                signal.signal(signal.SIGINT, self._handle_orchestrator_signal)
                signal.signal(signal.SIGTERM, self._handle_orchestrator_signal)
            except ValueError as e:
                print(f"Orchestrator ({self.pod_identifier}): Warning - Could not set signal handlers: {e}. ", flush=True)
            except Exception as e_sig:
                 print(f"Orchestrator ({self.pod_identifier}): Error setting signal handlers: {e_sig}", flush=True)
        else:
            print(f"Orchestrator ({self.pod_identifier}): Not running in main thread (Thread ID: {threading.get_ident()}). "
                  f"Skipping signal handler registration. Shutdown will be managed by _shutdown_flag.", flush=True)

        for i in range(self.num_partitions):
            partition_id = i
            worker_id_str = f"{self.pod_identifier}-p{partition_id}"

            process = multiprocessing.Process(
                target=start_worker_process,
                args=(partition_id, worker_id_str, self.handler_modules), # MODIFIED: Pass handler_modules
                daemon=True,
            )
            self.processes.append(process)
            process.start()
            print(
                f"Orchestrator ({self.pod_identifier}): Worker for partition {partition_id} (Consumer ID: {worker_id_str}) started with PID {process.pid}",
                flush=True
            )

        print(f"Orchestrator ({self.pod_identifier}): All workers started. Monitoring...", flush=True)
        try:
            while not self._shutdown_flag.is_set():
                for i, p in enumerate(self.processes):
                    if not p.is_alive():
                        print(
                            f"¡ALERT! Orchestrator ({self.pod_identifier}): Worker for partition {i} (Initial PID {p.pid}) unexpectedly terminated.",
                            flush=True
                        )
                if self._shutdown_flag.is_set():
                    print(f"Orchestrator ({self.pod_identifier}): Shutdown flag detected in monitoring loop. Exiting.", flush=True)
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print(
                f"Orchestrator ({self.pod_identifier}): KeyboardInterrupt received in orchestrator's main loop. Starting shutdown.",
                flush=True
            )
            self._shutdown_flag.set()
        except Exception as e_loop:
            print(f"Orchestrator ({self.pod_identifier}): Unexpected error in monitoring loop: {e_loop}. Forcing shutdown.", flush=True)
            self._shutdown_flag.set()
        finally:
            print(f"Orchestrator ({self.pod_identifier}): Exited monitoring loop. Calling stop().", flush=True)
            self.stop()

    def stop(self):
        print(
            f"Orchestrator ({self.pod_identifier}): Initiating shutdown of worker processes...",
            flush=True
        )
        self._shutdown_flag.set() 

        for i, process in enumerate(self.processes):
            if process.is_alive():
                print(
                    f"Orchestrator ({self.pod_identifier}): Attempting to join worker for partition {i} (PID {process.pid})...",
                    flush=True
                )
                process.join(timeout=10)
                if process.is_alive():
                    print(
                        f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (PID {process.pid}) did not terminate after 10s, forcing termination (SIGTERM)...",
                        flush=True
                    )
                    try:
                        process.terminate()
                        process.join(timeout=5)
                    except Exception as e_term:
                        print(f"Orchestrator ({self.pod_identifier}): Error during SIGTERM for worker {i} (PID {process.pid}): {e_term}", flush=True)

                    if process.is_alive():
                        print(
                            f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (PID {process.pid}) still alive after SIGTERM, sending SIGKILL...",
                            flush=True
                        )
                        try:
                            process.kill()
                            process.join(timeout=2)
                        except Exception as e_kill:
                            print(f"Orchestrator ({self.pod_identifier}): Error during SIGKILL for worker {i} (PID {process.pid}): {e_kill}", flush=True)
                else:
                    print(
                        f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (PID {process.pid}) joined correctly.",
                        flush=True
                    )
            else:
                print(
                    f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (Initial PID {process.pid}) was already terminated.",
                    flush=True
                )
        print(f"Orchestrator ({self.pod_identifier}): All worker processes stopped.", flush=True)

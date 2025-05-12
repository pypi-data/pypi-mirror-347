import multiprocessing
import time
import signal
import os
import threading

# Relative imports of your qtask_py package
from . import config
from .worker import start_worker_process
from .qtask import qtask, NoHandlerRegisteredError


class StreamOrchestrator:
    def __init__(self, num_workers_per_partition: int = 1):
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
        # Unique identifier for this orchestrator instance
        # Includes the PID of the process and the thread ID for greater uniqueness if executed in the same process.
        self.pod_identifier = os.getenv("POD_NAME", f"pod-{os.getpid()}-{threading.get_ident()}")


        # Validation to ensure that at least one message handler is registered.
        if not qtask.is_any_handler_registered():
            critical_error_message = (
                f"CRITICAL ERROR when starting Orchestrator ({self.pod_identifier}): No message handler has been registered.\n"
                "Ensure that you have defined at least one function with the @qtask.handler('topic_name') decorator "
                "in your main script before creating an instance of StreamOrchestrator."
            )
            print(critical_error_message, flush=True)
            raise NoHandlerRegisteredError("No topic handler has been registered in the system.")
        else:
            print(f"Orchestrator ({self.pod_identifier}): At least one message handler has been registered. Proceeding...", flush=True)
            
    def _handle_orchestrator_signal(self, signum, frame):
        # This handler is for when the orchestrator is the main process.
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

        # --- KEY MODIFICATION ---
        # Only register signal handlers if we are in the main thread of the main interpreter.
        if threading.current_thread() is threading.main_thread():
            print(f"Orchestrator ({self.pod_identifier}): Running in main thread. Registering signal handlers for SIGINT and SIGTERM.", flush=True)
            try:
                signal.signal(signal.SIGINT, self._handle_orchestrator_signal)
                signal.signal(signal.SIGTERM, self._handle_orchestrator_signal)
            except ValueError as e:
                # This might happen if not in the main thread of the main interpreter or during shutdown.
                print(f"Orchestrator ({self.pod_identifier}): Warning - Could not set signal handlers: {e}. "
                      "This might happen if not in the main thread of the main interpreter or during shutdown.", flush=True)
            except Exception as e_sig: # Catch other possible exceptions from signal.signal
                 print(f"Orchestrator ({self.pod_identifier}): Error setting signal handlers: {e_sig}", flush=True)
        else:
            print(f"Orchestrator ({self.pod_identifier}): Not running in main thread (Thread ID: {threading.get_ident()}). "
                  f"Skipping signal handler registration. Shutdown will be managed by _shutdown_flag.", flush=True)
        # --- END OF KEY MODIFICATION ---

        for i in range(self.num_partitions):
            partition_id = i
            # The worker_id_str must be globally unique if multiple orchestrators compete for the same consumer group.
            # self.pod_identifier already contributes to uniqueness.
            worker_id_str = f"{self.pod_identifier}-p{partition_id}"

            process = multiprocessing.Process(
                target=start_worker_process,
                args=(partition_id, worker_id_str), # worker_id_str is the consumer_id for Redis
                daemon=True, # Daemon processes terminate when the parent process terminates
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
                        # The original worker_id_str for this worker
                        # original_worker_id = f"{self.pod_identifier}-p{i}" # Assuming that 'i' is partition_id
                        print(
                            f"¡ALERT! Orchestrator ({self.pod_identifier}): Worker for partition {i} (Initial PID {p.pid}) unexpectedly terminated.",
                            flush=True
                        )
                        # Here you could implement restart logic if needed.
                        # For example, you could remove it from self.processes and launch a new one,
                        # or simply set self._shutdown_flag.set() to stop everything.
                        # For simplicity, this example does not restart workers.
                        # Consider: self._shutdown_flag.set() # To stop everything if a worker dies.
                if self._shutdown_flag.is_set():
                    print(f"Orchestrator ({self.pod_identifier}): Shutdown flag detected in monitoring loop. Exiting.", flush=True)
                    break
                time.sleep(1) # Check every second
        except KeyboardInterrupt:
            # This KeyboardInterrupt is primarily for when the orchestrator is executed directly
            # (e.g. as a main script) and Ctrl+C is pressed.
            print(
                f"Orchestrator ({self.pod_identifier}): KeyboardInterrupt received in orchestrator's main loop. Starting shutdown.",
                flush=True
            )
            self._shutdown_flag.set()
        except Exception as e_loop: # Catch any other exception in the monitoring loop
            print(f"Orchestrator ({self.pod_identifier}): Unexpected error in monitoring loop: {e_loop}. Forcing shutdown.", flush=True)
            self._shutdown_flag.set() # Force shutdown in case of unexpected error
        finally:
            # This 'finally' block ensures that stop() is called regardless of how the loop exits.
            print(f"Orchestrator ({self.pod_identifier}): Exited monitoring loop. Calling stop().", flush=True)
            self.stop()

    def stop(self):
        print(
            f"Orchestrator ({self.pod_identifier}): Initiating shutdown of worker processes...",
            flush=True
        )
        # Ensure that the shutdown flag is active for the workers as well,
        # although the workers should listen to their own shutdown_event.
        # The main purpose here is to make join to the worker processes.
        self._shutdown_flag.set() # Ensure the flag is set in case

        for i, process in enumerate(self.processes):
            # original_worker_id = f"{self.pod_identifier}-p{i}"
            if process.is_alive():
                print(
                    f"Orchestrator ({self.pod_identifier}): Attempting to join worker for partition {i} (PID {process.pid})...",
                    flush=True
                )
                process.join(timeout=10) # Wait for the worker process to terminate
                if process.is_alive():
                    print(
                        f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (PID {process.pid}) did not terminate after 10s, forcing termination (SIGTERM)...",
                        flush=True
                    )
                    try:
                        process.terminate() # Send SIGTERM
                        process.join(timeout=5) # Wait again
                    except Exception as e_term:
                        print(f"Orchestrator ({self.pod_identifier}): Error during SIGTERM for worker {i} (PID {process.pid}): {e_term}", flush=True)

                    if process.is_alive():
                        print(
                            f"Orchestrator ({self.pod_identifier}): Worker for partition {i} (PID {process.pid}) still alive after SIGTERM, sending SIGKILL...",
                            flush=True
                        )
                        try:
                            process.kill() # Send SIGKILL
                            process.join(timeout=2) # Final wait
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


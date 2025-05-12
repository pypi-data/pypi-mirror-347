import multiprocessing
import time
import signal
import os
from . import config
from .worker import start_worker_process
# Import the qtask instance and the specific exception
from .qtask import qtask, NoHandlerRegisteredError


class StreamOrchestrator:
    def __init__(self, num_workers_per_partition: int = 1):
        if num_workers_per_partition != 1:
            print(
                "Warning: This example is simplified for 1 worker per partition."
            )
            print(
                "For multiple pods competing, the generated consumer_id MUST be globally unique."
            )

        self.num_partitions = config.NUMBER_OF_PARTITIONS
        self.processes = []
        self._shutdown_flag = multiprocessing.Event()
        self.pod_identifier = os.getenv("POD_NAME", f"pod-{os.getpid()}")

        # --- ADJUSTED VALIDATION ---
        # Verify that AT LEAST ONE message handler is registered in the system.
        # The validation of whether a specific TOPIC has a handler
        # will be done by each worker when processing a message.
        if not qtask.is_any_handler_registered(): # We use the new method of the QTask class
            critical_error_message = (
                f"CRITICAL ERROR when starting Orchestrator ({self.pod_identifier}): No message handler has been registered.\n"
                "Ensure that you have defined at least one function with the @qtask.handler('topic_name') decorator "
                "in your main script before creating an instance of StreamOrchestrator."
            )
            print(critical_error_message)
            # We reuse NoHandlerRegisteredError or we could create a more generic one like NoHandlersAvailableError
            raise NoHandlerRegisteredError("No topic handler has been registered in the system.") 
        else:
            print(f"Orchestrator ({self.pod_identifier}): At least one message handler per topic has been registered. Proceeding...")
        # --- END OF ADJUSTED VALIDATION ---
            
    def _handle_orchestrator_signal(self, signum, frame):
        print(
            f"Orchestrator ({self.pod_identifier}): Signal {signum} received. Starting shutdown of workers..."
        )
        self._shutdown_flag.set()

    def start(self):
        print(
            f"Orchestrator ({self.pod_identifier}) starting {self.num_partitions} workers..."
        )

        signal.signal(signal.SIGINT, self._handle_orchestrator_signal)
        signal.signal(signal.SIGTERM, self._handle_orchestrator_signal)

        for i in range(self.num_partitions):
            partition_id = i
            worker_id_str = f"{self.pod_identifier}-p{partition_id}"

            process = multiprocessing.Process(
                target=start_worker_process,
                args=(partition_id, worker_id_str),
                daemon=True,
            )
            self.processes.append(process)
            process.start()
            print(
                f"Orchestrator ({self.pod_identifier}): Worker for partition {partition_id} (Consumer ID: {worker_id_str}) started with PID {process.pid}"
            )

        print(f"Orchestrator ({self.pod_identifier}): All workers started.")
        try:
            while not self._shutdown_flag.is_set():
                for i, p in enumerate(self.processes):
                    expected_consumer_id = f"{self.pod_identifier}-p{i}" # Assuming that i is partition_id
                    if not p.is_alive():
                        print(
                            f"¡ALERT! ({self.pod_identifier}) Worker for partition {i} (Consumer ID: {expected_consumer_id}, PID {p.pid}) unexpectedly terminated."
                        )
                        # Here you could implement restart logic if needed.
                        # For example, you could remove it from self.processes and launch a new one,
                        # or simply set self._shutdown_flag.set() to stop everything.
                if self._shutdown_flag.is_set():
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print(
                f"Orchestrator ({self.pod_identifier}): KeyboardInterrupt received, starting shutdown."
            )
            self._shutdown_flag.set()
        finally:
            self.stop()

    def stop(self):
        print(
            f"Orchestrator ({self.pod_identifier}): Sending shutdown signal to workers..."
        )
        for i, process in enumerate(self.processes):
            expected_consumer_id = f"{self.pod_identifier}-p{i}" # Assuming that i is partition_id
            print(
                f"Attempting to join worker for partition {i} (Consumer ID: {expected_consumer_id}, PID {process.pid})..."
            )
            process.join(timeout=10)
            if process.is_alive():
                print(
                    f"Worker for partition {i} (PID {process.pid}) did not terminate, forcing termination..."
                )
                process.terminate()
                process.join(timeout=2)
            else:
                print(
                    f"Worker for partition {i} (PID {process.pid}) joined correctly."
                )
        print(f"Orchestrator ({self.pod_identifier}): All workers stopped.")
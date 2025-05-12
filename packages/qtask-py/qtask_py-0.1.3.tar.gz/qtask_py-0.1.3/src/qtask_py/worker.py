import asyncio
import redis.asyncio as redis_async
from redis import exceptions as redis_exceptions
import json
import signal
import os
import importlib # MODIFIED: Added importlib

# Relative imports from your qtask_py package
from . import config
from .utils import get_partitioned_stream_name
from .qtask import qtask, NoHandlerRegisteredError # This will be the worker's local qtask instance

# Event to handle the shutdown signal
shutdown_event = asyncio.Event()

def handle_signal(signum, frame):
    worker_pid = os.getpid()
    print(f"Signal {signum} received in worker PID {worker_pid}, starting shutdown of worker...", flush=True)
    shutdown_event.set()

async def run_worker(partition_id: int, globally_unique_consumer_id: str):
    stream_name = get_partitioned_stream_name(partition_id)
    consumer_name = globally_unique_consumer_id
    worker_pid = os.getpid()

    # At this point, qtask instance for this worker process is initialized but likely has no handlers.
    # The handlers should have been loaded by importlib in start_worker_process.
    if not qtask.is_any_handler_registered():
        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): CRITICAL - No handlers were registered "
              "after attempting to load specified handler modules. This worker may not process any tasks.", flush=True)
    else:
        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Handlers successfully registered in this worker. "
              f"Known topics: {list(qtask._topic_handlers.keys())}", flush=True)


    r = redis_async.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT,
        db=config.REDIS_DB, decode_responses=False
    )

    try:
        await r.xgroup_create(
            name=stream_name,
            groupname=config.CONSUMER_GROUP_NAME,
            id='0',
            mkstream=True
        )
        print(f"Worker {consumer_name} (PID {worker_pid}): Group {config.CONSUMER_GROUP_NAME} ensured/created for stream {stream_name}", flush=True)
    except redis_exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"Worker {consumer_name} (PID {worker_pid}): Group {config.CONSUMER_GROUP_NAME} already exists for stream {stream_name}", flush=True)
        else:
            print(f"Worker {consumer_name} (PID {worker_pid}): Error creating group for {stream_name}: {e}", flush=True)
            await r.aclose()
            return

    print(f"Worker {consumer_name} (PID {worker_pid}) started for partition {partition_id} (stream: {stream_name}). Waiting for messages...", flush=True)

    while not shutdown_event.is_set():
        try:
            messages = await r.xreadgroup(
                groupname=config.CONSUMER_GROUP_NAME,
                consumername=consumer_name,
                streams={stream_name: '>'},
                count=config.MESSAGES_PER_READ,
                block=config.BLOCK_TIMEOUT_MS
            )

            if not messages:
                continue

            message_ids_to_ack = []
            for _stream_name_recv, msg_list in messages:
                for msg_id, msg_data_raw in msg_list:
                    message_id_str = msg_id.decode()
                    try:
                        original_partition_key = msg_data_raw.get(b'message_key', b'N/A').decode()
                        data_json_str = msg_data_raw.get(b'data', b'{}').decode()
                        full_message_data = json.loads(data_json_str)
                        
                        message_topic = full_message_data.get("topic")
                        message_payload_for_handler = full_message_data.get("payload", {})
                        
                        message_payload_for_handler['_metadata'] = {
                            'redis_message_id': message_id_str,
                            'partition_key_used': original_partition_key,
                            'stream_name': stream_name,
                            'consumer_name': consumer_name
                        }

                        if not message_topic:
                            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                                  f"Message ID {message_id_str} does not have a 'topic' field. Skipping and ACK.", flush=True)
                            message_ids_to_ack.append(msg_id)
                            continue
                        
                        # print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                        #       f"Received ID {message_id_str}, Topic: '{message_topic}'") # Less verbose

                        try:
                            message_handler_func = qtask.get_message_handler(message_topic)
                        except NoHandlerRegisteredError:
                            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                                  f"No handler registered for topic '{message_topic}' of message ID {message_id_str}. "
                                  "Skipping and ACK.", flush=True)
                            message_ids_to_ack.append(msg_id)
                            continue
                        
                        result = await message_handler_func(message_payload_for_handler)
                        
                        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                              f"Processed ID {message_id_str} (Topic: '{message_topic}') by '{message_handler_func.__name__}'.", flush=True)
                              # f"Result: {result}") # Result can be verbose
                        message_ids_to_ack.append(msg_id)

                    except json.JSONDecodeError as e_json:
                        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Error decoding JSON for message {message_id_str}: {e_json}", flush=True)
                        message_ids_to_ack.append(msg_id) 
                    except Exception as e_proc:
                        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Error processing message {message_id_str} (Topic: {message_topic if 'message_topic' in locals() else 'N/A'}): {e_proc}", flush=True)
                        # Decide on ACK strategy for processing errors. Not ACKing means retry.
                        pass 

            if message_ids_to_ack:
                await r.xack(stream_name, config.CONSUMER_GROUP_NAME, *message_ids_to_ack)

        except redis_exceptions.TimeoutError:
            continue
        except ConnectionRefusedError: 
            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Redis connection refused. Retrying in 5s...", flush=True)
            await asyncio.sleep(5)
        except redis_exceptions.RedisError as e_redis:
             print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Redis error: {e_redis}", flush=True)
             await asyncio.sleep(1) 
        except Exception as e_generic: 
            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Unexpected error: {e_generic}", flush=True)
            await asyncio.sleep(1)
        
        await asyncio.sleep(0.01)

    print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}) shutting down...", flush=True)
    await r.aclose()
    print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}) shut down.", flush=True)

# MODIFIED: Added handler_modules argument
def start_worker_process(partition_id: int, worker_id_str: str, handler_modules: list[str] | None = None):
    worker_pid = os.getpid()
    print(f"Worker process (PID {worker_pid}) for partition {partition_id} (Consumer ID: {worker_id_str}) started.", flush=True)

    # Configure signal handlers for this child process
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # MODIFIED: Import handler modules to register handlers in this worker process
    if handler_modules:
        print(f"Worker (PID {worker_pid}): Attempting to load handler modules: {handler_modules}", flush=True)
        for module_name in handler_modules:
            try:
                importlib.import_module(module_name)
                print(f"Worker (PID {worker_pid}): Successfully loaded handler module '{module_name}'.", flush=True)
            except ImportError as e_import:
                print(f"Worker (PID {worker_pid}): CRITICAL - Failed to import handler module '{module_name}': {e_import}", flush=True)
            except Exception as e_load:
                print(f"Worker (PID {worker_pid}): CRITICAL - Error loading handler module '{module_name}': {e_load}", flush=True)
    else:
        print(f"Worker (PID {worker_pid}): No specific handler modules provided to load.", flush=True)
        
    # The qtask instance is global within qtask.py, so decorators in imported modules will affect it.
    asyncio.run(run_worker(partition_id, worker_id_str))

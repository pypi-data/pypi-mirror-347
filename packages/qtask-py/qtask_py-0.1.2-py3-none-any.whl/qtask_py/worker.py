import asyncio
import redis.asyncio as redis_async
from redis import exceptions as redis_exceptions
import json
import signal
import os # Necessary for os.getpid() in handle_signal if used
from . import config
from .utils import get_partitioned_stream_name
# Import the qtask instance and the specific exception
from .qtask import qtask, NoHandlerRegisteredError

# Event to handle the shutdown signal
shutdown_event = asyncio.Event()

def handle_signal(signum, frame):
    # Adding the PID to the log is useful when you have multiple workers
    worker_pid = os.getpid()
    print(f"Signal {signum} received in worker PID {worker_pid}, starting shutdown of worker...")
    shutdown_event.set()

async def run_worker(partition_id: int, globally_unique_consumer_id: str):
    stream_name = get_partitioned_stream_name(partition_id)
    consumer_name = globally_unique_consumer_id
    worker_pid = os.getpid() # For clearer logs

    # The general validation of whether any handler exists already was done by the orchestrator.
    # Here, the worker will resolve the specific handler for each message.
    # We don't need to call qtask.get_message_handler() globally at the beginning of the worker.

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
        print(f"Worker {consumer_name} (PID {worker_pid}): Group {config.CONSUMER_GROUP_NAME} ensured/created for stream {stream_name}")
    except redis_exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"Worker {consumer_name} (PID {worker_pid}): Group {config.CONSUMER_GROUP_NAME} already exists for stream {stream_name}")
        else:
            print(f"Worker {consumer_name} (PID {worker_pid}): Error creating group for {stream_name}: {e}")
            await r.aclose()
            return

    print(f"Worker {consumer_name} (PID {worker_pid}) started for partition {partition_id} (stream: {stream_name}). Waiting for messages with topics...")

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
            for _stream_name_recv, msg_list in messages: # Although we only expect one stream here
                for msg_id, msg_data_raw in msg_list:
                    message_id_str = msg_id.decode() # Decode ID for logs
                    try:
                        # msg_data_raw is a dictionary of bytes, e.g.:
                        # {b'message_key': b'partition_key', b'data': b'{"topic":"EMAIL", "payload":{...}}'}
                        
                        # Extract the original partitioning key (optional, but you have it)
                        original_partition_key = msg_data_raw.get(b'message_key', b'N/A').decode()
                        
                        # Extract and deserialize the 'data' field
                        data_json_str = msg_data_raw.get(b'data', b'{}').decode()
                        full_message_data = json.loads(data_json_str)
                        
                        # --- ROUTING LOGIC BY TOPIC ---
                        message_topic = full_message_data.get("topic")
                        # The payload is what is actually passed to the specific topic handler.
                        # It can be the whole full_message_data or a part of it, like full_message_data.get("payload", {})
                        message_payload_for_handler = full_message_data.get("payload", {})
                        
                        # Optional: add metadata to the payload that receives the handler
                        message_payload_for_handler['_metadata'] = {
                            'redis_message_id': message_id_str,
                            'partition_key_used': original_partition_key,
                            'stream_name': stream_name,
                            'consumer_name': consumer_name
                        }

                        if not message_topic:
                            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                                  f"Message ID {message_id_str} does not have a 'topic' field. Skipping and doing ACK.")
                            message_ids_to_ack.append(msg_id)
                            continue
                        
                        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                              f"Received ID {message_id_str}, Topic: '{message_topic}', Partition Key: {original_partition_key}")

                        try:
                            # Get the specific handler for the message topic
                            message_handler_func = qtask.get_message_handler(message_topic)
                        except NoHandlerRegisteredError:
                            # If there is no handler for this topic, we log it and do ACK to not process it again.
                            # Consider a Dead Letter Queue (DLQ) for these cases in production.
                            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                                  f"No handler registered for topic '{message_topic}' of message ID {message_id_str}. "
                                  "Skipping and doing ACK.")
                            message_ids_to_ack.append(msg_id)
                            continue
                        
                        # Call the specific topic handler with its payload
                        result = await message_handler_func(message_payload_for_handler)
                        
                        print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): "
                              f"Processed ID {message_id_str} (Topic: '{message_topic}') by '{message_handler_func.__name__}', "
                              f"Result: {result}")
                        message_ids_to_ack.append(msg_id)
                        # --- END OF ROUTING LOGIC ---

                    except json.JSONDecodeError as e_json:
                        print(f"Error decoding JSON for message {message_id_str} in {consumer_name} (PID {worker_pid}, Stream {stream_name}): {e_json} - Raw data: {msg_data_raw}")
                        message_ids_to_ack.append(msg_id) # ACK to not process indefinitely if malformed
                    except Exception as e_proc: # Errors within the handler or logic of this loop
                        print(f"Error processing message {message_id_str} in {consumer_name} (PID {worker_pid}, Stream {stream_name}): {e_proc}")
                        # Not doing ACK allows retries/reclaiming. Consider DLQ or retry limit.
                        pass 

            if message_ids_to_ack:
                ack_result = await r.xack(stream_name, config.CONSUMER_GROUP_NAME, *message_ids_to_ack)
                # print(f"Worker {consumer_name} ({stream_name}): ACK for {len(message_ids_to_ack)} messages, result: {ack_result}")

        except redis_exceptions.TimeoutError:
            continue
        except ConnectionRefusedError: 
            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Redis connection refused. Retrying in 5s...")
            await asyncio.sleep(5)
        except redis_exceptions.RedisError as e_redis:
             print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Redis error in main loop: {e_redis}")
             await asyncio.sleep(1) 
        except Exception as e_generic: 
            print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}): Unexpected error in main loop: {e_generic}")
            await asyncio.sleep(1)
        
        await asyncio.sleep(0.01) # Small pause to yield control and avoid busy-loop

    print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}) shutting down...")
    await r.aclose()
    print(f"Worker {consumer_name} (PID {worker_pid}, Stream {stream_name}) shut down.")

def start_worker_process(partition_id: int, worker_id_str: str): # worker_id_str here is the globally_unique_consumer_id
    # Configure signal handlers for this child process
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    asyncio.run(run_worker(partition_id, worker_id_str))
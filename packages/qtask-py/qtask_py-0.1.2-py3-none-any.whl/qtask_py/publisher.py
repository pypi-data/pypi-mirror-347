import redis.asyncio as redis
import json
from . import config
from .utils import get_partitioned_stream_name, get_partition_for_message

class StreamPublisher:
    def __init__(self, redis_client: redis.Redis = None):
        self._redis = redis_client
        self._is_external_client = redis_client is not None

    async def _connect(self):
        if self._redis is None:
            self._redis = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_DB,
                decode_responses=False # Important for streams, manually decode
            )

    async def publish(self, message_key: str, data: dict, max_len: int = 10000):
        """
        Publishes a message to the appropriate partition.
        message_key: Used to determine the partition.
        data: Dictionary with the message data.
        max_len: Approximately, for XTRIM.
        """
        if self._redis is None:
            await self._connect()

        partition_id = get_partition_for_message(message_key)
        stream_name = get_partitioned_stream_name(partition_id)

        message_payload = {
            # We save the original key in case it is useful in the consumer
            b'message_key': message_key.encode('utf-8'),
            b'data': json.dumps(data).encode('utf-8')
        }
        try:
            message_id = await self._redis.xadd(
                name=stream_name,
                fields=message_payload,
                maxlen=max_len,
                approximate=True # Necessary if maxlen is used
            )
            print(f"Published message ID {message_id.decode()} to {stream_name} (key: {message_key})")
            return message_id.decode()
        except Exception as e:
            print(f"Error publishing to {stream_name}: {e}")
            return None

    async def close(self):
        if self._redis and not self._is_external_client:
            await self._redis.aclose()
            self._redis = None

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
"""
qtask - Simple messaging broker that uses Redis streams
"""

__version__ = "0.1.2"

from .publisher import StreamPublisher
from .orchestrator import StreamOrchestrator
from .config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    BASE_STREAM_NAME,
    NUMBER_OF_PARTITIONS,
    CONSUMER_GROUP_NAME,
)
from .utils import get_partition_for_message, get_partitioned_stream_name

from .qtask import qtask, NoHandlerRegisteredError

# Optional: define __all__
__all__ = [
    "StreamOrchestrator",
    "StreamPublisher",
    "config",
    "qtask",
    "NoHandlerRegisteredError",
    "get_partition_for_message",
    "get_partitioned_stream_name",
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_DB",
    "BASE_STREAM_NAME",
    "NUMBER_OF_PARTITIONS",
    "CONSUMER_GROUP_NAME",
    "__version__",
]

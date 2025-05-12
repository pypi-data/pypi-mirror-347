from . import config

def get_partitioned_stream_name(partition_id: int) -> str:
    """Generates the name of the stream for a specific partition."""
    if not 0 <= partition_id < config.NUMBER_OF_PARTITIONS:
        raise ValueError("Invalid partition ID")
    return f"{config.BASE_STREAM_NAME}:{partition_id}"

def get_partition_for_message(message_key: str) -> int:
    """Determines to which partition a message should go based on a key.
    Simple example using hash. You could use a more sophisticated logic.
    """
    return hash(message_key) % config.NUMBER_OF_PARTITIONS
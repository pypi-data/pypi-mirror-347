import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Base name for partitioned streams
BASE_STREAM_NAME = "my_app_stream"
NUMBER_OF_PARTITIONS = int(os.getenv('NUMBER_OF_PARTITIONS', 4)) # Example: 4 partitions
CONSUMER_GROUP_NAME = "my_processing_group"

# For workers
MESSAGES_PER_READ = 10 # How many messages to read per batch
BLOCK_TIMEOUT_MS = 2000 # How long to block waiting for messages
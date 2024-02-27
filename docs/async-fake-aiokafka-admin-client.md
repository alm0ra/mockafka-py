## FakeAIOKafkaAdmin Class

### Description
The `FakeAIOKafkaAdmin` class is a mock implementation of aiokafka's `AIOKafkaAdminClient`. It allows mocking Kafka administration operations for testing purposes.

### Parameters
- **clean (bool):** Whether to clean/reset the underlying `KafkaStore` on init. Default is False.

### Methods

#### `__init__(self, clean: bool = False, *args, **kwargs)`
- **Description:** Initializes the `FakeAIOKafkaAdmin`.
- **Parameters:**
  - `clean (bool):` Whether to clean/reset the underlying `KafkaStore` on init. Default is False.
  - `*args, **kwargs`: Additional arguments.

#### `close(self)`
- **Description:** Closes the admin client.

#### `start(self)`
- **Description:** Starts the admin client.

#### `_create_topic(self, topic: NewTopic) -> None`
- **Description:** Creates a topic in the underlying `KafkaStore`.
- **Parameters:**
  - `topic (NewTopic):` NewTopic object containing name and num_partitions.

#### `_remove_topic(self, topic: str)`
- **Description:** Deletes a topic from the underlying `KafkaStore` by name.
- **Parameters:**
  - `topic (str):` Name of the topic to delete.

#### `create_topics(self, new_topics: list[NewTopic], *args, **kwargs)`
- **Description:** Creates multiple topics from a list of `NewTopic` objects. Calls `_create_topic()` for each one.
- **Parameters:**
  - `new_topics (list[NewTopic]):` List of `NewTopic` objects.

#### `delete_topics(self, topics: list[str], **kwargs) -> None`
- **Description:** Deletes multiple topics by name from a list of strings. Calls `_remove_topic()` for each one.
- **Parameters:**
  - `topics (list[str]):` List of topic names to delete.

#### `_create_partition(self, topic: str, partition_count: int)`
- **Description:** Adds partitions to a topic in `KafkaStore`.
- **Parameters:**
  - `topic (str):` Name of the topic.
  - `partition_count (int):` Number of partitions to add.

#### `create_partitions(self, topic_partitions: Dict[str, NewPartitions], *args, **kwargs)`
- **Description:** Adds partitions to multiple topics from a dictionary mapping topic name to `NewPartitions` object containing `total_count`. Calls `_create_partition()` for each topic.
- **Parameters:**
  - `topic_partitions (Dict[str, NewPartitions]):` Dictionary mapping topic name to `NewPartitions` object.

### Example Usage

```python
from aiokafka import NewTopic, NewPartitions
from mockafka.aiokafka import FakeAIOKafkaAdmin

# Create an instance of FakeAIOKafkaAdmin
fake_admin = FakeAIOKafkaAdmin()

# Define new topics
new_topics = [NewTopic(name='topic1', num_partitions=3), NewTopic(name='topic2', num_partitions=5)]

# Create topics
await fake_admin.create_topics(new_topics=new_topics)

# Define additional partitions for topics
topic_partitions = {'topic1': NewPartitions(total_count=5), 'topic2': NewPartitions(total_count=7)}

# Add partitions to topics
await fake_admin.create_partitions(topic_partitions=topic_partitions)
```

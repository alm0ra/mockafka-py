## KafkaStore Class

### Description
The `KafkaStore` class represents an in-memory simulation of a Kafka store. It includes methods for managing topics, partitions, offsets, and producing/consuming messages.

### Properties
- **mock_topics**: A dictionary to store topics, each containing partitions and associated messages.
- **offset_store**: A dictionary to store offset information for each topic and partition.

### Methods

#### `__init__(self, clean: bool = False)`
- **Description:** Initializes the KafkaStore.
- **Parameters:**
  - `clean` (bool): If True, clears existing mock topics and offset store.

#### `is_topic_exist(topic: str) -> bool`
- **Description:** Checks if a topic exists.
- **Parameters:**
  - `topic` (str): The name of the topic.
- **Returns:** (bool) True if the topic exists, False otherwise.

#### `is_partition_exist_on_topic(topic: str, partition_num: int) -> bool`
- **Description:** Checks if a partition exists in a given topic.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition_num` (int): The partition number.
- **Returns:** (bool) True if the partition exists, False otherwise.

#### `get_number_of_partition(topic: str) -> int`
- **Description:** Gets the number of partitions in a topic.
- **Parameters:**
  - `topic` (str): The name of the topic.
- **Returns:** (int) The number of partitions in the topic.

#### `create_topic(topic: str)`
- **Description:** Creates a new topic.
- **Parameters:**
  - `topic` (str): The name of the topic.

#### `create_partition(self, topic: str, partitions: int)`
- **Description:** Creates partitions for a topic.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partitions` (int): The number of partitions to create.

#### `remove_topic(self, topic: str)`
- **Description:** Removes a topic and its associated partitions.
- **Parameters:**
  - `topic` (str): The name of the topic.

#### `set_first_offset(self, topic: str, partition: int, value: int)`
- **Description:** Sets the first offset for a partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
  - `value` (int): The offset value.

#### `_add_next_offset(self, topic: str, partition: int)`
- **Description:** Increments the next offset for a partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.

#### `get_offset_store_key(self, topic: str, partition: int) -> str`
- **Description:** Generates the key for offset storage.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
- **Returns:** (str) Offset store key.

#### `produce(self, message: Message, topic: str, partition: int)`
- **Description:** Produces a message to a specific topic and partition.
- **Parameters:**
  - `message` (Message): The message to produce.
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.

#### `get_message(self, topic: str, partition: int, offset: int) -> Message`
- **Description:** Gets a message from a specific topic, partition, and offset.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
  - `offset` (int): The offset of the message.
- **Returns:** (Message) The requested message.

#### `get_partition_first_offset(self, topic: str, partition: int) -> int`
- **Description:** Gets the first offset for a partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
- **Returns:** (int) The first offset for the partition.

#### `get_partition_next_offset(self, topic: str, partition: int) -> int`
- **Description:** Gets the next offset for a partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
- **Returns:** (int) The next offset for the partition.

#### `topic_list() -> list[str]`
- **Description:** Gets the list of existing topics.
- **Returns:** (list[str]) List of topic names.

#### `partition_list(topic: str) -> list[int]`
- **Description:** Gets the list of partitions for a given topic.
- **Parameters:**
  - `topic` (str): The name of the topic.
- **Returns:** (list[int]) List of partition numbers.

#### `get_messages_in_partition(topic: str, partition: int) -> list[Message]`
- **Description:** Gets all messages in a specific partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.
- **Returns:** (list[Message]) List of messages in the partition.

#### `number_of_message_in_topic(self, topic: str) -> int`
- **Description:** Gets the total number of messages in a topic.
- **Parameters:**
  - `topic` (str): The name of the topic.
- **Returns:** (int) The total number of messages in the topic.

#### `clear_topic_messages(self, topic: str)`
- **Description:** Clears all messages in a topic.
- **Parameters:**
  - `topic` (str): The name of the topic.

#### `clear_partition_messages(topic: str, partition: int)`
- **Description:** Clears all messages in a specific partition.
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `partition` (int): The partition number.

#### `reset_offset(self, topic: str, strategy: str = 'latest')`
- **Description:** Resets offsets for a topic based on a strategy (latest or earliest).
- **Parameters:**
  - `topic` (str): The name of the topic.
  - `strategy` (str): The offset reset strategy ('latest' or 'earliest').

#### `fresh()`
- **Description:** Clears all mock topics and offset stores, essentially starting fresh.

### Example Usage

```python
# Create an instance of KafkaStore
kafka_store = KafkaStore()

# Create a topic and partitions
kafka_store.create_topic('sample_topic')
kafka_store.create_partition('sample_topic', 4)

# Produce a message to a specific partition
message = Message(content='Hello, Kafka!')
kafka_store.produce(message, 'sample_topic', 1)

# Get a message from a specific topic, partition, and offset
retrieved_message = kafka_store.get_message('sample_topic', 1, 0)


## FakeConsumer Class

### Description
The `FakeConsumer` class is a mock implementation of the Confluent Kafka Consumer designed for testing purposes. It uses an in-memory storage (`KafkaStore`) to simulate Kafka behavior. The class includes methods for consuming, committing, listing topics, polling for messages, and managing subscriptions.

### Properties
- **kafka**: An instance of the `KafkaStore` class for in-memory storage.
- **consumer_store**: A dictionary to store consumer offsets for each topic-partition.
- **subscribed_topic**: A list of topics subscribed by the consumer.

### Methods

#### `__init__(self, *args, **kwargs)`
- **Description:** Initializes the `FakeConsumer`.
- **Parameters:**
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).

#### `consume(self, num_messages=1, *args, **kwargs) -> Message or None`
- **Description:** Consumes messages from subscribed topics.
- **Parameters:**
  - `num_messages` (int): Number of messages to consume.
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Returns:** (Message or None) Consumed message or None if no message is available.

#### `close(self, *args, **kwargs)`
- **Description:** Closes the consumer and resets state.
- **Parameters:**
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).

#### `commit(self, message: Message = None, *args, **kwargs)`
- **Description:** Commits offsets for consumed messages.
- **Parameters:**
  - `message` (Message): Consumed message (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).

#### `list_topics(self, topic=None, *args, **kwargs) -> ClusterMetadata`
- **Description:** Lists topics and returns `ClusterMetadata`.
- **Parameters:**
  - `topic`: Topic name (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Returns:** (ClusterMetadata) Metadata of the listed topics.

#### `poll(self, timeout=None) -> Message or None`
- **Description:** Polls for messages from subscribed topics.
- **Parameters:**
  - `timeout` (float): Poll timeout in seconds.
- **Returns:** (Message or None) Consumed message or None if no message is available.

#### `_get_key(self, topic, partition) -> str`
- **Description:** Generates a unique key for a topic-partition pair.
- **Parameters:**
  - `topic`: Topic name.
  - `partition`: Partition number.
- **Returns:** (str) Unique key for the topic-partition pair.

#### `subscribe(self, topics, on_assign=None, *args, **kwargs)`
- **Description:** Subscribes to one or more topics.
- **Parameters:**
  - `topics` (list): List of topics to subscribe to.
  - `on_assign`: Callback function for partition assignments (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Raises:** (KafkaException) If a subscribed topic does not exist in the Kafka store.

#### `unsubscribe(self, *args, **kwargs)`
- **Description:** Unsubscribes from one or more topics.
- **Parameters:**
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments.

#### `assign(self, partitions)`
- **Description:** Assigns partitions to the consumer (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to assign (unused).

#### `unassign(self, *args, **kwargs)`
- **Description:** Unassigns partitions (unsupported in mockafka).
- **Parameters:**
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).

#### `assignment(self, *args, **kwargs) -> list`
- **Description:** Gets assigned partitions (unsupported in mockafka).
- **Returns:** (list) An empty list.

#### `committed(self, partitions, timeout=None) -> list`
- **Description:** Gets committed offsets (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to get committed offsets for (unused).
  - `timeout`: Timeout for the operation (unused).
- **Returns:** (list) An empty list.

#### `get_watermark_offsets(self, partition, timeout=None, *args, **kwargs) -> tuple`
- **Description:** Gets watermark offsets (unsupported in mockafka).
- **Parameters:**
  - `partition`: Partition to get watermark offsets for (unused).
  - `timeout`: Timeout for the operation (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Returns:** (tuple) Tuple with watermark offsets (0, 0).

#### `offsets_for_times(self, partitions, timeout=None) -> list`
- **Description:** Gets offsets for given times (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to get offsets for (unused).
  - `timeout`: Timeout for the operation (unused).
- **Returns:** (list) An empty list.

#### `pause(self, partitions) -> None`
- **Description:** Pauses consumption from specified partitions (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to pause consumption from (unused).
- **Returns:** (None)

#### `position(self, partitions) -> list`
- **Description:** Gets the current position of the consumer in specified partitions (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to get position for (unused).
- **Returns:** (list) An empty list.

#### `resume(self, partitions) -> None`
- **Description:** Resumes consumption from specified partitions (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to resume consumption from (unused).
- **Returns:** (None)

#### `seek(self, partition) -> None`
- **Description:** Seeks to a specific offset in a partition (unsupported in mockafka).
- **Parameters:**
  - `partition`: Partition to seek in (unused).

#### `store_offsets(self, message=None, *args, **kwargs) -> None`
- **Description:** Stores offsets for consumed messages (unsupported in mockafka).
- **Parameters:**
  - `message`: Consumed message (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Returns:** (None)

#### `consumer_group_metadata(self) -> None`
- **Description:** Gets consumer group metadata (unsupported in mockafka).
- **Returns:** (None)

#### `incremental_assign(self, partitions) -> None`
- **Description:** Incrementally assigns partitions (unsupported in mockafka).
- **Parameters:**
  - `partitions`: Partitions to incrementally assign (unused).
- **Returns:** (None)

#### `incremental_unassign(self, partitions) -> None`
- **Description:** Incrementally unassigns partitions (unsupported in mockafka).
- **Parameters:**
  -

 `partitions`: Partitions to incrementally unassign (unused).
- **Returns:** (None)

### Example Usage

```python
# Create an instance of FakeConsumer
fake_consumer = FakeConsumer()

# Subscribe to topics
fake_consumer.subscribe(topics=['sample_topic'])

# Consume messages
consumed_message = fake_consumer.consume()

# Commit offsets
fake_consumer.commit()

# Unsubscribe from topics
fake_consumer.unsubscribe(topics=['sample_topic'])

# Close the consumer
fake_consumer.close()
```
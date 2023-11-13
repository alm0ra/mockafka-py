## FakeProducer Class

### Description
The `FakeProducer` class is a mock implementation of the Confluent Kafka Producer for testing purposes. It uses an in-memory storage (`KafkaStore`) to simulate Kafka behavior. The class includes methods for producing messages, listing topics, and handling transactions.

### Properties
- **kafka**: An instance of the `KafkaStore` class for in-memory storage.

### Methods

#### `__init__(self, config: dict = None)`
- **Description:** Initializes the `FakeProducer`.
- **Parameters:**
  - `config` (dict): Configuration for the producer (unused).

#### `produce(self, topic, value=None, *args, **kwargs)`
- **Description:** Produces messages to a specified topic.
- **Parameters:**
  - `topic`: Topic to produce messages to.
  - `value`: Message value (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments, including the partition for the message.

#### `list_topics(self, topic=None, *args, **kwargs) -> ClusterMetadata`
- **Description:** Lists topics and returns `ClusterMetadata`.
- **Parameters:**
  - `topic`: Topic name (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).
- **Returns:** (ClusterMetadata) Metadata of the listed topics.

#### `abort_transaction(self, timeout=None)`
- **Description:** Aborts a transaction (unsupported in mockafka).
- **Parameters:**
  - `timeout`: Timeout for the operation (unused).

#### `begin_transaction(self)`
- **Description:** Begins a transaction (unsupported in mockafka).

#### `commit_transaction(self, timeout=None)`
- **Description:** Commits a transaction (unsupported in mockafka).
- **Parameters:**
  - `timeout`: Timeout for the operation (unused).

#### `flush(self, timeout=None) -> int`
- **Description:** Flushes the producer (unsupported in mockafka).
- **Parameters:**
  - `timeout`: Timeout for the operation (unused).
- **Returns:** (int) Always returns 0.

#### `init_transactions(self, timeout=None)`
- **Description:** Initializes transactions (unsupported in mockafka).
- **Parameters:**
  - `timeout`: Timeout for the operation (unused).

#### `poll(self, timeout=None) -> int`
- **Description:** Polls for events (unsupported in mockafka).
- **Parameters:**
  - `timeout`: Timeout for the operation (unused).
- **Returns:** (int) Always returns 0.

#### `purge(self, in_queue=True, *args, **kwargs)`
- **Description:** Purges messages (unsupported in mockafka).
- **Parameters:**
  - `in_queue`: Purge messages in the queue (unused).
  - `args`: Additional arguments (unused).
  - `kwargs`: Additional keyword arguments (unused).

#### `send_offsets_to_transaction(self, positions, group_metadata, timeout=None)`
- **Description:** Sends offsets to a transaction (unsupported in mockafka).
- **Parameters:**
  - `positions`: Offset positions (unused).
  - `group_metadata`: Group metadata (unused).
  - `timeout`: Timeout for the operation (unused).

### Example Usage

```python
from mockafka import FakeProducer

# Create an instance of FakeProducer
fake_producer = FakeProducer()

# Produce a message
fake_producer.produce(topic='sample_topic', value='Hello, Kafka!', partition=0)

```
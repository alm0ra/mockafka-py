## FakeAIOKafkaConsumer Class

### Description
The `FakeAIOKafkaConsumer` class is a mock implementation of aiokafka's AIOKafkaConsumer. It allows mocking a Kafka consumer for testing purposes.

### Parameters
- **args, kwargs:** Passed to superclass init, not used here.

### Attributes
- **kafka:** A `KafkaStore` instance for underlying storage.
- **consumer_store (dict):** Tracks consumption progress per topic/partition.
- **subscribed_topic (list):** List of subscribed topic names.

### Methods

#### `__init__(self, *args, **kwargs)`
- **Description:** Initializes the `FakeAIOKafkaConsumer`.
- **Parameters:**
  - `args, kwargs`: Passed to superclass init, not used here.

#### `start(self)`
- **Description:** Resets the internal state.

#### `stop(self)`
- **Description:** Resets the internal state.

#### `commit(self)`
- **Description:** Commits offsets to `KafkaStore` by updating `first_offset`.

#### `topics(self)`
- **Description:** Gets subscribed topics.

#### `subscribe(self, topics: list[str])`
- **Description:** Subscribes to topics by name.

#### `subscription(self) -> list[str]`
- **Description:** Gets subscribed topics.

#### `unsubscribe(self)`
- **Description:** Resets subscribed topics.

#### `getone(self)`
- **Description:** Gets the next available message from subscribed topics. Updates `consumer_store` as messages are consumed.

#### `getmany(self)`
- **Description:** Currently just calls `getone()`.

### Example Usage

```python
from mockafka.aiokafka import FakeAIOKafkaConsumer

# Create an instance of FakeAIOKafkaConsumer
fake_consumer = FakeAIOKafkaConsumer()

# Subscribe to topics
fake_consumer.subscribe(topics=['sample_topic1', 'sample_topic2'])

# start consumer 
await fake_consumer.start()

# Get one message
message = await fake_consumer.getone()
```

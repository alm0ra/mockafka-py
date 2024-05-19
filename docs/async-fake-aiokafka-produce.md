## FakeAIOKafkaProducer Class

### Description
The `FakeAIOKafkaProducer` class is a mock implementation of aiokafka's AIOKafkaProducer. It allows mocking a Kafka producer for testing purposes.

### Parameters
- **args, kwargs:** Passed to superclass init, not used here.

### Attributes
- **kafka:** A `KafkaStore` instance for underlying storage.

### Methods

#### `__init__(self, *args, **kwargs)`
- **Description:** Initializes the `FakeAIOKafkaProducer`.
- **Parameters:**
  - `args, kwargs`: Passed to superclass init, not used here.

#### `_produce(self, topic, value=None, *args, **kwargs)`
- **Description:** Create a `Message` and produce it to `KafkaStore`.
- **Parameters:**
  - `topic`: Topic to produce the message to.
  - `value`: Message value.
  - `args`: Additional arguments.
  - `kwargs`: Additional keyword arguments, including the partition for the message.

#### `start(self)`
- **Description:** No-operation.

#### `stop(self)`
- **Description:** No-operation.

#### `send(self, *args, **kwargs)`
- **Description:** Calls `_produce()` with keyword arguments.
- **Parameters:**
  - `args, kwargs`: Arguments and keyword arguments passed to `_produce()`.

#### `send_and_wait(self, *args, **kwargs)`
- **Description:** Calls `send()`.
- **Parameters:**
  - `args, kwargs`: Arguments and keyword arguments passed to `send()`.

### Example Usage

```python

from mockafka.aiokafka import FakeAIOKafkaProducer

# Create an instance of FakeAIOKafkaProducer
fake_producer = FakeAIOKafkaProducer()

# Produce a message
await fake_producer.send(topic='sample_topic', value='Hello, Kafka!', partition=0)
```

### `@aconsume` Decorator

This decorator is designed for simulating asynchronous message consumption using a `FakeAIOKafkaConsumer`. It subscribes to specified topics and consumes messages in a loop. For each message consumed, it calls the decorated function with the message as a keyword argument. After consuming all available messages, it calls the decorated function again without the message argument.

#### Parameters:
- `topics (list[str])`: List of topic names to subscribe to.
- `auto_commit (bool)`: Whether to automatically commit offsets after consuming messages. Default is True.

#### Example Usage:
```python
from mockafka import aconsume

@aconsume(topics=['test'], auto_commit=False)
async def process_message(message):
    # message processing logic
```

### `@aproduce` Decorator

This decorator is for simulating message production using a `FakeAIOKafkaProducer`. It creates a `FakeAIOKafkaProducer` instance and calls `send()` to produce a message with the provided parameters. Then, it calls the decorated function.

#### Parameters:
- `**decorator_args`: Arguments for producing the message, including:
  - `topic (str)`: Topic to produce to.
  - `value (str)`: Message value.
  - `key (str)`: Message key.
  - `headers (dict)`: Message headers.
  - `partition (int)`: Topic partition to produce to.

#### Example Usage:
```python
from mockafka import aproduce

@aproduce(topic='test', value='foo')
async def produce_message():
    # test logic here
```

### `@asetup_kafka` Decorator

This decorator is for setting up mock Kafka topics using a `FakeAIOKafkaAdminClient`. It takes a list of topic configurations, each containing the topic name and partition count, and an option to clean existing topics first. It creates the specified topics using a `FakeAIOKafkaAdminClient`.

#### Parameters:
- `topics (list[dict]):` List of topic configurations, each containing:
  - `topic (str)`: Topic name.
  - `partition (int)`: Partition count.
- `clean (bool):` Whether to clean existing topics first. Default is False.

#### Example Usage:

```python
from mockafka import asetup_kafka

@asetup_kafka(topics=[{'topic': 'test', 'partition': 1}])
async def test_function():
    # test logic
```


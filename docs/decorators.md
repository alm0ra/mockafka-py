## Decorators Documentation

### `@setup_kafka` Decorator

This decorator is designed for setting up Mockafka with specified topics using a `FakeAdminClient`. It allows you to define topics and their partitions and choose whether to start with a clean Kafka (remove existing topics) or not.

#### Parameters:
- `topics (list[dict[str, str]])`: A list of dictionaries containing topic details. Each dictionary should have the keys 'topic' and 'partition'.
- `clean (bool)`: Option to have a clean Kafka (remove existing topics) or not.

#### Example Usage:
```python
@setup_kafka(topics=[{'topic': 'test_topic', 'partition': 5}], clean=True)
def test_function():
    # Your test logic here
```

### `@produce` Decorator

This decorator simulates message production using a `FakeProducer`. It allows you to specify the topic, value, key, headers, and partition of the produced message.

#### Parameters:
- `topic (str)`: The topic to produce the message.
- `value (str)`: The value of the message.
- `key (str)`: The key of the message.
- `headers (str)`: The headers of the message.
- `partition (str)`: The partition of the topic.

#### Example Usage:
```python
@produce(topic='test_topic', value='test_value', key='test_key', headers=None, partition=0)
def test_function():
    # Your test logic here
```

### `@consume` Decorator

This decorator simulates message consumption using a `FakeConsumer`. It allows you to subscribe to specified topics and provides the consumed message to the decorated function.

#### Parameters:
- `topics (list[str])`: A list of topics to subscribe to.
- `auto_commit (bool)`: Whether to automatically commit offsets after consuming messages.

#### Example Usage:
```python
@consume(topics=['test_topic'], auto_commit=False)
def test_function(message):
    # Your test logic for processing the consumed message here
```

### `@bulk_produce` Decorator

This decorator is for bulk-producing messages using a `FakeProducer`. It allows you to specify a list of dictionaries containing message details such as value, key, topic, partition, timestamp, and headers.

#### Parameters:
- `list_of_messages (list[dict[str, str]])`: A list of dictionaries containing message details.

#### Example Usage:
```python
@bulk_produce(list_of_messages=[{'topic': 'test_topic', 'value': 'test_value1'}, {...}])
def test_function():
    # Your test logic here
```

Feel free to use these decorators in your test functions to set up, produce, consume, and bulk-produce messages in a Mockafka environment.


## Multi-Decorator Examples Documentation

In the following examples, we showcase the usage of multiple decorators to simulate different scenarios in a Mockafka environment. These scenarios include producing, consuming, and setting up Kafka topics using the provided decorators.

### Example 1: Using `@produce` and `@consume` Decorators

#### Test Case: `test_produce_decorator`
```python
from mockafka import produce, consume

@produce(topic='test', key='test_key', value='test_value', partition=4)
@consume(topics=['test'])
def test_produce_and_consume_decorator(message):
    """
    This test showcases the usage of both @produce and @consume decorators in a single test case.
    It produces a message to the 'test' topic and then consumes it to perform further logic.
    # Notice you may got message None
    """
    # Your test logic for processing the consumed message here
    
    if not message:
        return 
    
    pass

```

### Example 2: Using Multiple `@produce` Decorators

#### Test Case: `test_produce_twice`
```python
from mockafka import produce

@produce(topic='test', key='test_key', value='test_value', partition=4)
@produce(topic='test', key='test_key1', value='test_value1', partition=0)
def test_produce_twice():
    # Your test logic here
    pass
```

### Example 3: Using `@bulk_produce` and `@consume` Decorators

#### Test Case: `test_bulk_produce_decorator`
```python
from mockafka import bulk_produce, consume

@bulk_produce(list_of_messages=sample_for_bulk_produce)
@consume(topics=['test'])
def test_bulk_produce_and_consume_decorator(message):
    """
    This test showcases the usage of both @bulk_produce and @consume decorators in a single test case.
    It bulk produces messages to the 'test' topic and then consumes them to perform further logic.
    """
    # Your test logic for processing the consumed message here
    pass

```

### Example 4: Using `@setup_kafka` and `@produce` Decorators

#### Test Case: `test_produce_with_kafka_setup_decorator`
```python
from mockafka import setup_kafka, produce

@setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
@produce(topic='test_topic', partition=5, key='test_', value='test_value1')
def test_produce_with_kafka_setup_decorator():
    # Your test logic here
    pass
```

### Example 5: Using `@setup_kafka`, Multiple `@produce`, and `@consume` Decorators

#### Test Case: `test_consumer_decorator`
```python
from mockafka import setup_kafka, produce, consume

@setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
@produce(topic='test_topic', partition=5, key='test_', value='test_value1')
@produce(topic='test_topic', partition=5, key='test_', value='test_value1')
@consume(topics=['test_topic'])
def test_consumer_decorator(message: Message = None):
    if message is None:
        return
    # Your test logic for processing the consumed message here
    pass
```

Feel free to adapt these examples to your specific test cases and scenarios. The provided decorators aim to simplify the setup and execution of tests in a Mockafka environment.
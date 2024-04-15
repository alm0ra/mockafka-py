![Alt text](banner.png)
<p align="center">
    <em>Mockafka-py is a Python library designed for in-memory mocking of Kafka.</em>
</p>

![PyPI - Downloads](https://img.shields.io/pypi/dm/mockafka-py)
![Codecov](https://img.shields.io/codecov/c/github/alm0ra/mockafka-py)
[![CodeFactor](https://www.codefactor.io/repository/github/alm0ra/mockafka-py/badge)](https://www.codefactor.io/repository/github/alm0ra/mockafka-py)
[![codebeat badge](https://codebeat.co/badges/9cda14cf-3aac-438f-a6f7-c67517d7d74f)](https://codebeat.co/projects/github-com-alm0ra-mockafka-py-main)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/alm0ra/mockafka-py/python-app.yml)
![GitHub](https://img.shields.io/github/license/alm0ra/mockafka-py)
![GitHub release (with filter)](https://img.shields.io/github/v/release/alm0ra/mockafka-py)
![GitHub repo size](https://img.shields.io/github/repo-size/alm0ra/mockafka-py)

# Mockafka: Fake Version for confluent-kafka-python & aiokafka

# Features

- Compatible with confluent-kafka
- Compatible with aiokafka (async support)
- Supports Produce, Consume, and AdminClient operations with ease.


# Getting Start

### Installing via pip or poetry

```bash
pip install mockafka-py

# or using poetry
poetry add mockafka-py
```


# Usage

## Multi-Decorator Examples for `confluent-kafka-python`

In the following examples, we showcase the usage of multiple decorators to simulate different scenarios in a Mockafka
environment. These scenarios include producing, consuming, and setting up Kafka topics using the provided decorators.

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
    # Notice you may get message None
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
    It does bulk produces messages to the 'test' topic and then consumes them to perform further logic.
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

## Using classes like confluent-kafka

```python
from mockafka import FakeProducer, FakeConsumer, FakeAdminClientImpl
from mockafka.admin_client import NewTopic
from random import randint

# Create topic
admin = FakeAdminClientImpl()
admin.create_topics([
    NewTopic(topic='test', num_partitions=5)
])

# Produce messages
producer = FakeProducer()
for i in range(0, 10):
    producer.produce(
        topic='test',
        key=f'test_key{i}',
        value=f'test_value{i}',
        partition=randint(0, 4)
    )

# Subscribe consumer
consumer = FakeConsumer()
consumer.subscribe(topics=['test'])

# Consume messages
while True:
    message = consumer.poll()
    print(message)
    consumer.commit()

    if message is None:
        break
```

Output:

```
"""
<mockafka.message.Message object at 0x7fe84b4c3310>
<mockafka.message.Message object at 0x7fe84b4c3370>
<mockafka.message.Message object at 0x7fe84b4c33a0>
<mockafka.message.Message object at 0x7fe84b4c33d0>
<mockafka.message.Message object at 0x7fe84b4c3430>
<mockafka.message.Message object at 0x7fe84b4c32e0>
<mockafka.message.Message object at 0x7fe84b4c31f0>
<mockafka.message.Message object at 0x7fe84b4c32b0>
<mockafka.message.Message object at 0x7fe84b4c3400>
<mockafka.message.Message object at 0x7fe84b4c3340>
None
"""
```
# Async support
## Multi-Decorator Examples for `aiokafka`

### Example 1: Using `@aproduce` and `@aconsume` and `@asetup_kafka` Decorators

#### Test Case: `test_produce_and_consume_with_decorator`

```python
import pytest
from mockafka import aproduce, aconsume, asetup_kafka


@pytest.mark.asyncio
@asetup_kafka(topics=[{'topic': 'test_topic', 'partition': 16}], clean=True)
@aproduce(topic='test_topic', value='test_value', key='test_key', partition=0)
@aconsume(topics=['test_topic'])
async def test_produce_and_consume_with_decorator(message=None):
    if not message:
        return

    assert message.key() == 'test_key'
    assert message.value() == 'test_value'
```

### Example 2: Using `@aproduce` and `@asetup_kafka` Decorators

#### Test Case: `test_produce_with_decorator`

```python
import pytest
from mockafka import aproduce, asetup_kafka
from mockafka.aiokafka import FakeAIOKafkaConsumer

@pytest.mark.asyncio
@asetup_kafka(topics=[{'topic': 'test_topic', 'partition': 16}], clean=True)
@aproduce(topic='test_topic', value='test_value', key='test_key', partition=0)
async def test_produce_with_decorator():
    consumer = FakeAIOKafkaConsumer()
    await consumer.start()
    consumer.subscribe(['test_topic'])
    message = await consumer.getone()

    assert message.key() == 'test_key'
    assert message.value() == 'test_value'
```

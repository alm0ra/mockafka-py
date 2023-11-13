
![Alt text](banner.png)
<p align="center">
    <em>Mockafka-py is a Python library designed for in-memory mocking of Kafka.</em>
</p>

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/alm0ra/mockafka-py/python-app.yml)
![GitHub](https://img.shields.io/github/license/alm0ra/mockafka-py)
![Codecov](https://img.shields.io/codecov/c/github/alm0ra/mockafka-py)
![GitHub release (with filter)](https://img.shields.io/github/v/release/alm0ra/mockafka-py)



# Mockafka: Fake Version of confluent-kafka-python

# Features
- Compatible with confluent-kafka
- Supports Produce, Consume, and AdminClient operations with ease.

# TODO

# Getting Start

### Installing via pip

```bash
pip install mockafka-py
```

# Usage

## Using decorators in pytest

### `@setup_kafka` decorator 
This decorator is used to prepare Mockafka and create topics more conveniently. The parameters are:

- `topics` : A list of topics to create.
- `clean` : Option to have a clean Kafka or clean all data in Kafka.

usage: 
```python
from mockafka import setup_kafka

@setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
def test_produce_with_kafka_setup_decorator():
    # topics are already created
    pass
```

### `@produce` decorator 
This decorator is used for producing events in Mockafka more easily for testing. Parameters include:

`topic` The topic to produce the message.
`value` The value of the message.
`key`  The key of the message.
`headers` The headers of the message.
`partition` The partition of the topic.

Example:
```python
from mockafka import produce

@produce(topic='test_topic', partition=5, key='test_', value='test_value1')
def test_produce_with_kafka_setup_decorator():
    # Message is already produced.
    pass
```

### `@bulk_produce` decorator 
This decorator is used for bulk-producing events in Mockafka more easily for testing. Parameters include a list of messages.
```
sample_for_bulk_produce = [
    {
        "key": "test_key",
        "value": "test_value",
        "topic": "test",
        "partition": 0,
    }
]
```

usage: 
```python
from mockafka import bulk_produce

@bulk_produce(list_of_messages=sample_for_bulk_produce)
def test_bulk_produce_decorator():
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
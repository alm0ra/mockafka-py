
![Alt text](banner.png)
<p align="center">
    <em>Mockafka-py is a python library for mocking kafka in memory</em>
</p>

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/alm0ra/mockafka-py/python-app.yml)
![GitHub](https://img.shields.io/github/license/alm0ra/mockafka-py)
![Codecov](https://img.shields.io/codecov/c/github/alm0ra/mockafka-py)
![GitHub release (with filter)](https://img.shields.io/github/v/release/alm0ra/mockafka-py)



# Mockafka 
fake version of confluent-kafka-python 

# Features
- compatible with confluent-kafka
- Produce, Consume, AdminClient operations with ease.

# TODO

# Getting Start

Installing using pip

```bash
pip install mockafka-py
```

# Usage

```python
from mockafka import FakeProducer, FakeConsumer, FakeAdminClientImpl
from mockafka.admin_client import NewTopic
from random import randint

# create topic
admin = FakeAdminClientImpl()
admin.create_topics([
    NewTopic(topic='test', num_partitions=5)
])

# produce message
producer = FakeProducer()
for i in range(0, 10):
    producer.produce(
        topic='test',
        key=f'test_key{i}',
        value=f'test_value{i}',
        partition=randint(0, 4)
    )

# subscribe consumer
consumer = FakeConsumer()
consumer.subscribe(topics=['test'])

# consume messages

while True:
    message = consumer.poll()
    print(message)
    consumer.commit()

    if message is None:
        break

"""
out put
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
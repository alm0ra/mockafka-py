
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

while True:
    message = consumer.poll()

    print(message)
    consumer.commit()

    if message is None:
        break
```
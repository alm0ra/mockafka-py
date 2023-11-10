
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
- Programmatically build MongoDB aggregation pipelines.
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

# create topic
FakeAdminClientImpl().create_topics([
    NewTopic(topic='sample-topic-1', num_partitions=4),
    NewTopic(topic='sample-topic-2', num_partitions=4),
])

```
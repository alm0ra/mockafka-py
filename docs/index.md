# Mockafka python lib

![Alt text](assets/banner.png)


# Getting Start

### Installing via pip

```bash
pip install mockafka-py
```

# Usage

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
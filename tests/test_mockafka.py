from mockafka import FakeProducer, FakeConsumer, FakeAdminClientImpl
from mockafka.admin_client import NewTopic
from random import randint

admin = FakeAdminClientImpl()
producer = FakeProducer()
consumer = FakeConsumer()

admin.create_topics([
    NewTopic(topic='test', num_partitions=5)
])

for i in range(0, 10):
    producer.produce(
        topic='test',
        key=f'test_key{i}',
        value=f'test_value{i}',
        partition=randint(0,4)
    )


while True:
    message = consumer.poll()
    print(message)
    consumer.commit()

    if message is None:
        break

import uuid
from random import randint, choice
from typing import Any

import pytest

from mockafka import FakeConsumer
from mockafka import FakeProducer, FakeAdminClientImpl
from mockafka.admin_client import NewTopic

KAFKA_TOPIC_AUDITS = "test_1"
KAFKA_TOPIC_RAW_DOCS = "test_2"


class MockConsumer:
    def __init__(self):
        self._consumer = FakeConsumer()

    def consume(self, topics, msg_cnt=1) -> Any:
        self._consumer.subscribe(topics)
        messages = []
        cnt = 1
        while cnt <= msg_cnt:
            message = self._consumer.poll(timeout=1.0)
            if message is not None:
                messages.append(message.value())
                cnt = cnt + 1
            self._consumer.commit(message)
        return messages

    def close(self):
        self._consumer.close()


class MockProducer:

    def __init__(self):
        admin = FakeAdminClientImpl(clean=True)
        admin.create_topics([
            NewTopic(topic=KAFKA_TOPIC_AUDITS, num_partitions=2),
            NewTopic(topic=KAFKA_TOPIC_RAW_DOCS, num_partitions=2)
        ])
        self._producer = FakeProducer()

    def produce(self, topic: str, key: str, message: dict):
        self._producer.produce(
            key=key + str(uuid.uuid4()),
            value=message,
            topic=topic,
            partition=randint(0, 1)
        )


@pytest.mark.parametrize("count", range(1200, 1240))
def test_consumer_consistency(count):
    producer = MockProducer()

    for i in range(count):
        producer.produce(
            topic=choice([KAFKA_TOPIC_AUDITS, KAFKA_TOPIC_RAW_DOCS]),
            key=str(i),
            message={"u": str(uuid.uuid4())},
        )

    consumer = MockConsumer()
    messages = consumer.consume(topics=[KAFKA_TOPIC_AUDITS, KAFKA_TOPIC_RAW_DOCS], msg_cnt=int(count))

    assert len(messages) == count

from __future__ import annotations

import pytest
from aiokafka.admin import NewTopic  # type: ignore[import-untyped]

from mockafka import aconsume, aproduce, asetup_kafka
from mockafka.aiokafka import (
    FakeAIOKafkaAdmin,
    FakeAIOKafkaConsumer,
    FakeAIOKafkaProducer,
)


# Here is a reference snippet of code from mockafka/aiokafka/aiokafka_admin.py:
@pytest.mark.asyncio
async def test_create_topics():
    admin_client = FakeAIOKafkaAdmin()
    await admin_client.create_topics(
        new_topics=[
            NewTopic(name="test_topic", num_partitions=1, replication_factor=1),
        ]
    )


# Here is a reference snippet of code from fake aiokafka producer consumer & admin client:
@pytest.mark.asyncio
async def test_produce_and_consume():
    # create topic via admin client
    admin_client = FakeAIOKafkaAdmin(clean=True)
    await admin_client.create_topics(
        new_topics=[
            NewTopic(name="test_topic", num_partitions=1, replication_factor=1),
        ]
    )

    # produce message via producer client
    producer = FakeAIOKafkaProducer()
    await producer.start()
    await producer.send(
        headers={},
        key="test_key",
        value="test_value",
        topic="test_topic",
        partition=0,
    )

    # consume message via consumer client
    consumer = FakeAIOKafkaConsumer()
    await consumer.start()
    consumer.subscribe(["test_topic"])
    message = await consumer.getone()

    assert message.key == b"test_key"
    assert message.value == b"test_value"

    message = await consumer.getone()

    assert message is None


@pytest.mark.asyncio
@asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}], clean=True)
@aproduce(topic="test_topic", value="test_value", key="test_key", partition=0)
async def test_produce_with_decorator():
    consumer = FakeAIOKafkaConsumer()
    await consumer.start()
    consumer.subscribe(["test_topic"])
    message = await consumer.getone()

    assert message.key == b"test_key"
    assert message.value == b"test_value"


@pytest.mark.asyncio
@asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}], clean=True)
@aproduce(topic="test_topic", value="test_value", key="test_key", partition=0)
@aconsume(topics=["test_topic"])
async def test_produce_and_consume_with_decorator(message=None):
    if not message:
        return

    assert message.key == b"test_key"
    assert message.value == b"test_value"


@pytest.mark.asyncio
@asetup_kafka(topics=[{"topic": "test_topic1", "partition": 2}], clean=True)
async def test_produce_and_consume_with_headers():
    producer = FakeAIOKafkaProducer()
    consumer = FakeAIOKafkaConsumer()

    await producer.start()
    await consumer.start()
    consumer.subscribe({"test_topic1"})

    await producer.send(
        topic="test_topic1",
        headers=[('header_name', b"test"), ('header_name2', b"test")],
    )
    await producer.stop()

    record = await consumer.getone()
    assert record.headers == (('header_name', b"test"), ('header_name2', b"test"))

    await consumer.stop()

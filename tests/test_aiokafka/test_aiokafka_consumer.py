from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

import pytest
from aiokafka.structs import TopicPartition  # type: ignore[import-untyped]

from mockafka.aiokafka import (
    FakeAIOKafkaConsumer,
    FakeAIOKafkaAdmin,
    FakeAIOKafkaProducer,
)
from mockafka.kafka_store import KafkaStore


@pytest.mark.asyncio
class TestAIOKAFKAFakeConsumer(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeAIOKafkaProducer()
        self.consumer = FakeAIOKafkaConsumer()
        self.admin = FakeAIOKafkaAdmin()
        self.test_topic = "test_topic"

    @pytest.fixture(autouse=True)
    def topic(self):
        self.test_topic = "test_topic"

    def create_topic(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=16)

    async def produce_message(self):
        await self.producer.send(
            topic=self.test_topic, partition=0, key="test", value="test"
        )
        await self.producer.send(
            topic=self.test_topic, partition=0, key="test1", value="test1"
        )

    async def test_consume(self):
        await self.test_poll_with_commit()

    async def test_start(self):
        # check consumer store is empty
        await self.consumer.start()
        self.assertEqual(self.consumer.consumer_store, {})

        # change consumer store and check it's changed
        self.consumer.consumer_store = {"key", "value"}
        self.assertNotEqual(self.consumer.consumer_store, {})

        # close consumer and check consumer store and consume return none
        await self.consumer.stop()
        self.assertEqual(self.consumer.consumer_store, {})
        self.assertIsNone(await self.consumer.getone())

    async def test_poll_without_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])

        message = await self.consumer.getone()
        self.assertEqual(message.value(payload=None), "test")
        message = await self.consumer.getone()
        self.assertEqual(message.value(payload=None), "test1")

        self.assertIsNone(await self.consumer.getone())
        self.assertIsNone(await self.consumer.getone())

    async def test_partition_specific_poll_without_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])

        message = await self.consumer.getone(
            TopicPartition(self.test_topic, 2),
        )
        self.assertIsNone(message)

        message = await self.consumer.getone(
            TopicPartition(self.test_topic, 0),
        )
        self.assertEqual(message.value(payload=None), "test")

    async def test_poll_with_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])

        message = await self.consumer.getone()
        await self.consumer.commit()
        self.assertEqual(message.value(payload=None), "test")

        message = await self.consumer.getone()
        await self.consumer.commit()
        self.assertEqual(message.value(payload=None), "test1")

        self.assertIsNone(await self.consumer.getone())
        self.assertIsNone(await self.consumer.getone())

    async def test_subscribe(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)

    async def test_subscribe_pattern(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        self.kafka.create_partition(topic="other_topic", partitions=10)

        self.consumer.subscribe(pattern=r"^test_.*")

        topics = [self.test_topic, test_topic_2]
        self.assertEqual(self.consumer.subscribed_topic, topics)

    async def test_subscribe_topic_not_exist(self):
        topics = [self.test_topic]
        self.consumer.subscribe(topics=topics)

    async def test_unsubscribe(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)
        self.consumer.unsubscribe()
        self.assertEqual(self.consumer.subscribed_topic, [])

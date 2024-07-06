from __future__ import annotations

import asyncio
from unittest import IsolatedAsyncioTestCase

import pytest
from aiokafka.admin import NewTopic

from mockafka import Message
from mockafka.aiokafka import (
    FakeAIOKafkaAdmin,
    FakeAIOKafkaConsumer,
    FakeAIOKafkaProducer,
)
from mockafka.decorators import aconsume, aproduce, asetup_kafka

sample_for_bulk_produce = [
    {
        "key": "test_key",
        "value": "test_value",
        "topic": "test",
        "partition": 0,
    },
    {
        "key": "test_key1",
        "value": "test_value1",
        "topic": "test",
        "partition": 1,
    },
]


@pytest.mark.asyncio
class TestDecorators(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.admin = FakeAIOKafkaAdmin(clean=True)
        asyncio.run(self._create_fake_topics())
        self.consumer = FakeAIOKafkaConsumer()
        self.producer = FakeAIOKafkaProducer()
        self.fake_producer = FakeAIOKafkaProducer()

    async def _create_fake_topics(self):
        await self.admin.create_topics(
            [NewTopic(name="test", num_partitions=16, replication_factor=1)]
        )

    @aproduce(topic="test", key="test_key", value="test_value", partition=4)
    async def test_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])
        message = await self.consumer.getone()

        self.assertEqual(message.value(payload=None), "test_value")
        self.assertEqual(message.key(), "test_key")

        # commit message and check
        await self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(await self.consumer.getone())

    @aproduce(topic="test", key="test_key", value="test_value", partition=4)
    @aproduce(topic="test", key="test_key1", value="test_value1", partition=0)
    async def test_produce_twice(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])

        # Order unknown as partition order is not predictable
        messages = [
            (x.key(), x.value(payload=None))
            for x in (
                await self.consumer.getone(),
                await self.consumer.getone(),
            )
        ]
        self.assertCountEqual(
            [
                ("test_key", "test_value"),
                ("test_key1", "test_value1"),
            ],
            messages,
        )

        # commit message and check
        await self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(await self.consumer.getone())

    @asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @aproduce(topic="test_topic", partition=5, key="test_", value="test_value1")
    async def test_produce_with_kafka_setup_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test_topic"])

        message = await self.consumer.getone()
        self.assertEqual(message.value(payload=None), "test_value1")
        self.assertEqual(message.key(), "test_")

    @asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @aproduce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @aproduce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @aconsume(topics=["test_topic"])
    async def test_consumer_decorator(self, message: Message = None):
        if message is None:
            return

        self.assertEqual(message.key(), "test_")
        self.assertEqual(message._partition, 5)

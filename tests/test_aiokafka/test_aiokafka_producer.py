from __future__ import annotations

from unittest import IsolatedAsyncioTestCase

import pytest
from aiokafka.admin import NewTopic  # type: ignore[import-untyped]

from mockafka import Message
from mockafka.aiokafka.aiokafka_admin_client import FakeAIOKafkaAdmin
from mockafka.aiokafka.aiokafka_producer import FakeAIOKafkaProducer
from mockafka.kafka_store import KafkaStore, KafkaException


@pytest.mark.asyncio
class TestFakeProducer(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeAIOKafkaProducer()
        self.admin_client = FakeAIOKafkaAdmin()

        self.topic = "test1"
        self.key = "test_key"
        self.value = "test_value"

    async def _create_mock_topic(self):
        await self.admin_client.create_topics(
            new_topics=[
                NewTopic(name="test1", num_partitions=4, replication_factor=1),
                NewTopic(name="test2", num_partitions=8, replication_factor=1),
                NewTopic(name="topic_test", num_partitions=8, replication_factor=1),
            ]
        )

    async def test_produce_failed_topic_not_exist(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={},
                key=self.key,
                value=self.value,
                topic="alaki",
                partition=0,
            )

    async def test_produce_on_partition_not_exist(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={},
                key=self.key,
                value=self.value,
                topic=self.topic,
                partition=17,
            )

    async def test_produce_fail_for_none_partition(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={},
                key=self.key,
                value=self.value,
                topic=self.topic,
                partition=None,
            )

    async def test_produce_once(self) -> None:
        await self._create_mock_topic()
        await self.producer.send(
            headers=[
                ("header-name1", b"header-value"),
                ("header-name2", None),
                ("header-name1", b"duplicate!"),
            ],
            key=self.key,
            value=self.value,
            topic=self.topic,
            partition=0,
        )
        message: Message = self.kafka.get_messages_in_partition(
            topic=self.topic, partition=0
        )[0]
        self.assertEqual(message.key(), self.key)
        self.assertEqual(message.value(payload=None), self.value)
        self.assertEqual(message.topic(), self.topic)
        self.assertEqual(
            message.headers(),
            [
                ("header-name1", b"header-value"),
                ("header-name2", None),
                ("header-name1", b"duplicate!"),
            ],
        )
        self.assertEqual(message.error(), None)
        self.assertEqual(message.latency(), None)

    async def test_send_and_wait(self) -> None:
        await self._create_mock_topic()

        await self.producer.start()
        try:
            await self.producer.send_and_wait("topic_test", "sdfjhasdfhjsa", key="datakey")
        finally:
            await self.producer.stop()

        message: Message = self.kafka.get_messages_in_partition(
            topic="topic_test", partition=0
        )[0]
        self.assertEqual(message.key(), "datakey")
        self.assertEqual(message.topic(), "topic_test")

    async def test_context_manager(self) -> None:
        await self._create_mock_topic()

        async with self.producer as producer:
            self.assertEqual(self.producer, producer)
            await self.producer.send_and_wait("topic_test", "skdfjh", key="datakey")

        message: Message = self.kafka.get_messages_in_partition(
            topic="topic_test",
            partition=0,
        )[0]
        self.assertEqual(message.key(), "datakey")
        self.assertEqual(message.topic(), "topic_test")

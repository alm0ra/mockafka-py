from unittest import TestCase

import pytest
from aiokafka.admin import NewTopic

from mockafka import Message
from mockafka.aiokafka.aiokafka_admin_client import FakeAIOKafkaAdmin
from mockafka.aiokafka.aiokafka_producer import FakeAIOKafkaProducer
from mockafka.kafka_store import KafkaStore, KafkaException


@pytest.mark.asyncio
class TestFakeProducer(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeAIOKafkaProducer()
        self.admin_client = FakeAIOKafkaAdmin()

        # create topic with partitions
        self.admin_client.create_topics(new_topics=[
            NewTopic(name='test1', num_partitions=4, replication_factor=1),
            NewTopic(name='test2', num_partitions=8, replication_factor=1),
        ])

    @pytest.fixture(autouse=True)
    def topic(self):
        self.topic = 'test1'

    @pytest.fixture(autouse=True)
    def key(self):
        self.key = 'test_key'

    @pytest.fixture(autouse=True)
    def value(self):
        self.value = 'test_value'

    async def test_produce_failed_topic_not_exist(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={}, key=self.key, value=self.value, topic='alaki', partition=0,
            )

    async def test_produce_on_partition_not_exist(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={}, key=self.key, value=self.value, topic=self.topic, partition=17,
            )

    async def test_produce_fail_for_none_partition(self):
        with pytest.raises(KafkaException):
            await self.producer.send(
                headers={}, key=self.key, value=self.value, topic=self.topic, partition=None,
            )

    async def test_produce_once(self):
        await self.producer.send(
            headers={}, key=self.key, value=self.value, topic=self.topic, partition=0,
        )
        message: Message = self.kafka.get_messages_in_partition(topic=self.topic, partition=0)[0]
        self.assertEqual(message.key(), self.key)
        self.assertEqual(message.value(payload=None), self.value)
        self.assertEqual(message.topic(), self.topic)
        self.assertEqual(message.headers(), {})
        self.assertEqual(message.error(), None)
        self.assertEqual(message.latency(), None)

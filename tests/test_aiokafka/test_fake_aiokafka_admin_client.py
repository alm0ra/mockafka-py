from unittest import IsolatedAsyncioTestCase

import pytest
from aiokafka.admin import NewTopic, NewPartitions

from mockafka.aiokafka.aiokafka_admin_client import FakeAIOKafkaAdmin
from mockafka.kafka_store import KafkaStore


@pytest.mark.asyncio
class TestFakeAIOKafkaAdminClient(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.admin = FakeAIOKafkaAdmin()
        self.test_partition = NewPartitions(total_count=16)
        self.test_topic = NewTopic(name="test", num_partitions=16, replication_factor=1)

    async def test_create_partitions(self):
        await self.admin.start()
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic from admin client
        await self.admin.create_partitions({self.test_topic.name: self.test_partition})

        # test there is not topic in mockafka
        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

        self.assertEqual(self.kafka.get_number_of_partition(topic="test"), 16)
        await self.admin.close()

    async def test_create_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic via admin client
        await self.admin.create_topics(new_topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

    async def test_delete_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic via admin client
        await self.admin.create_topics(new_topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

        # remove topic
        await self.admin.delete_topics(topics=[self.test_topic.name])

        # test topic is removed from kafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

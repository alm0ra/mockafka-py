from unittest import TestCase

import pytest

from mockafka.admin_client import FakeAdminClientImpl
from mockafka.conumser import FakeConsumer
from mockafka.kafka_store import KafkaStore
from mockafka.producer import FakeProducer


@pytest.mark.asyncio
class TestAIOKAFKAFakeConsumer(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeProducer()
        self.consumer = FakeConsumer()
        self.admin = FakeAdminClientImpl()

    @pytest.fixture(autouse=True)
    def topic(self):
        self.test_topic = 'test_topic'

    def create_topic(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=16)

    def produce_message(self):
        self.producer.produce(topic=self.test_topic, partition=0, key='test', value='test')
        self.producer.produce(topic=self.test_topic, partition=0, key='test1', value='test1')

    def test_consume(self):
        self.test_poll_with_commit()

    async def test_close(self):
        # check consumer store is empty
        self.assertEqual(self.consumer.consumer_store, {})

        # change consumer store and check it's changed
        self.consumer.consumer_store = {'key', 'value'}
        self.assertNotEqual(self.consumer.consumer_store, {})

        # close consumer and check consumer store and consume return none
        await self.consumer.close()
        self.assertEqual(self.consumer.consumer_store, {})
        self.assertIsNone(self.consumer.consume())

    async def test_poll_without_commit(self):
        self.create_topic()
        self.produce_message()
        await self.consumer.subscribe(topics=[self.test_topic])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test')
        message = await self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test')

        self.assertIsNone(self.consumer.poll())
        self.assertIsNone(self.consumer.poll())

    async def test_poll_with_commit(self):
        self.create_topic()
        self.produce_message()
        await self.consumer.subscribe(topics=[self.test_topic])

        message = await self.consumer.poll()
        await self.consumer.commit()
        self.assertEqual(message.value(payload=None), 'test')

        message = await self.consumer.poll()
        await self.consumer.commit()
        self.assertEqual(message.value(payload=None), 'test1')

        self.assertIsNone(self.consumer.poll())
        self.assertIsNone(self.consumer.poll())

    async def test_subscribe(self):
        test_topic_2 = 'test_topic_2'
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        topics = [self.test_topic, test_topic_2]
        await self.consumer.subscribe(topics=topics)

        self.assertEqual(
            self.consumer.subscribed_topic, topics
        )

    async def test_subscribe_topic_not_exist(self):
        topics = [self.test_topic]
        await self.consumer.subscribe(topics=topics)

    async def test_unsubscribe(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]
        await self.consumer.subscribe(topics=topics)

        self.assertEqual(
            self.consumer.subscribed_topic, topics
        )
        await self.consumer.unsubscribe()
        self.assertEqual(
            self.consumer.subscribed_topic, []
        )

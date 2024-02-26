from aiokafka.admin import NewTopic
from mockafka import Message
from mockafka.decorators import aconsume, aproduce, asetup_kafka
from mockafka.aiokafka import FakeAIOKafkaAdmin, FakeAIOKafkaConsumer, FakeAIOKafkaProducer
from unittest import TestCase

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
    }
]


class TestDecorators(TestCase):
    def setUp(self) -> None:
        self.admin = FakeAIOKafkaAdmin(clean=True)
        self.admin.create_topics([NewTopic(name='test', num_partitions=16, replication_factor=1)])
        self.consumer = FakeAIOKafkaConsumer()
        self.producer = FakeAIOKafkaProducer()
        self.fake_producer = FakeAIOKafkaProducer()

    @aproduce(topic='test', key='test_key', value='test_value', partition=4)
    async def test_produce_decorator(self):
        # subscribe to topic and get message
        await self.consumer.subscribe(topics=['test'])
        message = await self.consumer.getone()

        self.assertEqual(message.value(payload=None), 'test_value')
        self.assertEqual(message.key(), 'test_key')

        # commit message and check
        await self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(await self.consumer.getone())

    @aproduce(topic='test', key='test_key', value='test_value', partition=4)
    @aproduce(topic='test', key='test_key1', value='test_value1', partition=0)
    async def test_produce_twice(self):
        # subscribe to topic and get message
        await self.consumer.subscribe(topics=['test'])
        message = await self.consumer.poll()

        self.assertEqual(message.value(payload=None), 'test_value1')
        self.assertEqual(message.key(), 'test_key1')

        message = await self.consumer.getone()
        self.assertEqual(message.value(payload=None), 'test_value')
        self.assertEqual(message.key(), 'test_key')

        # commit message and check
        await self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(await self.consumer.getone())

    @asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @aproduce(topic='test_topic', partition=5, key='test_', value='test_value1')
    async def test_produce_with_kafka_setup_decorator(self):
        # subscribe to topic and get message
        await self.consumer.subscribe(topics=['test_topic'])

        message = await self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test_value1')
        self.assertEqual(message.key(), 'test_')

    @asetup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @aproduce(topic='test_topic', partition=5, key='test_', value='test_value1')
    @aproduce(topic='test_topic', partition=5, key='test_', value='test_value1')
    @aconsume(topics=['test_topic'])
    async def test_consumer_decorator(self, message: Message = None):
        if message is None:
            return

        self.assertEqual(message.key(), 'test_')
        self.assertEqual(message._partition, 5)

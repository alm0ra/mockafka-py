from mockafka import FakeConsumer, produce, bulk_produce
from mockafka.admin_client import FakeAdminClientImpl, NewTopic
from mockafka.producer import FakeProducer

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
        self.admin = FakeAdminClientImpl(clean=True)
        self.admin.create_topics([NewTopic(topic='test', num_partitions=16)])
        self.consumer = FakeConsumer()
        self.producer = FakeProducer()
        self.fake_producer = FakeProducer()

    @produce(topic='test', key='test_key', value='test_value', partition=4)
    def test_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=['test'])
        message = self.consumer.poll()

        self.assertEqual(message.value(payload=None), 'test_value')
        self.assertEqual(message.key(), 'test_key')

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @produce(topic='test', key='test_key', value='test_value', partition=4)
    @produce(topic='test', key='test_key1', value='test_value1', partition=0)
    def test_produce_twice(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=['test'])
        message = self.consumer.poll()

        self.assertEqual(message.value(payload=None), 'test_value1')
        self.assertEqual(message.key(), 'test_key1')

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test_value')
        self.assertEqual(message.key(), 'test_key')

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @bulk_produce(list_of_messages=sample_for_bulk_produce)
    def test_bulk_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=['test'])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test_value')
        self.assertEqual(message.key(), 'test_key')

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), 'test_value1')
        self.assertEqual(message.key(), 'test_key1')

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

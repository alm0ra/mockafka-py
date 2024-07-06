from __future__ import annotations

from mockafka import FakeConsumer, produce, bulk_produce, setup_kafka, Message
from mockafka.admin_client import FakeAdminClientImpl, NewTopic
from mockafka.producer import FakeProducer
from mockafka.decorators.consumer import consume
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
    },
]


class TestDecorators(TestCase):
    def setUp(self) -> None:
        self.admin = FakeAdminClientImpl(clean=True)
        self.admin.create_topics([NewTopic(topic="test", num_partitions=16)])
        self.consumer = FakeConsumer()
        self.producer = FakeProducer()
        self.fake_producer = FakeProducer()

    @produce(topic="test", key="test_key", value="test_value", partition=4)
    def test_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])
        message = self.consumer.poll()

        self.assertEqual(message.value(payload=None), "test_value")
        self.assertEqual(message.key(), "test_key")

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @produce(topic="test", key="test_key", value="test_value", partition=4)
    @produce(topic="test", key="test_key1", value="test_value1", partition=0)
    def test_produce_twice(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])

        # Order unknown as partition order is not predictable
        messages = [
            (x.key(), x.value(payload=None))
            for x in (
                self.consumer.poll(),
                self.consumer.poll(),
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
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @bulk_produce(list_of_messages=sample_for_bulk_produce)
    def test_bulk_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), "test_value")
        self.assertEqual(message.key(), "test_key")

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), "test_value1")
        self.assertEqual(message.key(), "test_key1")

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    def test_produce_with_kafka_setup_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test_topic"])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), "test_value1")
        self.assertEqual(message.key(), "test_")

    @setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @consume(topics=["test_topic"])
    def test_consumer_decorator(self, message: Message = None):
        if message is None:
            return

        self.assertEqual(message.key(), "test_")
        self.assertEqual(message._partition, 5)

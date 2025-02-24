from __future__ import annotations

from unittest import TestCase

import pytest

from mockafka.admin_client import FakeAdminClientImpl
from mockafka.consumer import FakeConsumer
from mockafka.kafka_store import KafkaStore
from mockafka.producer import FakeProducer


class TestFakeConsumer(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeProducer()
        self.consumer = FakeConsumer()
        self.admin = FakeAdminClientImpl()

    @pytest.fixture(autouse=True)
    def topic(self):
        self.test_topic = "test_topic"

    def create_topic(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=16)

    def produce_message(self):
        self.producer.produce(
            topic=self.test_topic, partition=0, key="test", value="test"
        )
        self.producer.produce(
            topic=self.test_topic, partition=0, key="test1", value="test1"
        )

    def test_consume(self):
        self.test_poll_with_commit()

    def test_close(self):
        # check consumer store is empty
        self.assertEqual(self.consumer.consumer_store, {})

        # change consumer store and check it's changed
        self.consumer.consumer_store = {"key", "value"}
        self.assertNotEqual(self.consumer.consumer_store, {})

        # close consumer and check consumer store and consume return none
        self.consumer.close()
        self.assertEqual(self.consumer.consumer_store, {})
        self.assertEqual(self.consumer.consume(), [])

    def test_consume_batch_without_commit(self):
        """ Test correct number of messages inside batch using `consume` method. """
        # GIVEN:
        #   - 10 messages inside topic
        number_of_message = 10
        self.create_topic()
        for _ in range(number_of_message):
            self.producer.produce(
                topic=self.test_topic, partition=0, key="test1", value="test1"
            )

        # WHEN:
        #   - consumer uses consume method to get a batch of messages
        self.consumer.subscribe(topics=[self.test_topic])
        messages = self.consumer.consume(num_messages=number_of_message)

        # THEN:
        #   - batch of messages has correct count of messages
        assert len(messages) == number_of_message

    def test_poll_without_commit(self):
        self.create_topic()
        self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), "test")
        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), "test1")

        self.assertIsNone(self.consumer.poll())
        self.assertIsNone(self.consumer.poll())

    def test_poll_with_commit(self):
        self.create_topic()
        self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])

        message = self.consumer.poll()
        self.consumer.commit()
        self.assertEqual(message.value(payload=None), "test")

        message = self.consumer.poll()
        self.consumer.commit()
        self.assertEqual(message.value(payload=None), "test1")

        self.assertIsNone(self.consumer.poll())
        self.assertIsNone(self.consumer.poll())

    def test_subscribe(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)

    def test_subscribe_topic_not_exist(self):
        topics = [self.test_topic]
        self.consumer.subscribe(topics=topics)

    def test_unsubscribe(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)
        self.consumer.unsubscribe(topics=topics)
        self.assertEqual(self.consumer.subscribed_topic, [])

    def test_assign(self):
        # This method Does not support in mockafka
        self.consumer.assign(partitions=None)

    def test_unassign(self):
        # This method Does not support in mockafka
        self.consumer.unassign()

    def test_assignment(self):
        # This method Does not support in mockafka
        self.consumer.assignment()

    def test_committed(self):
        # This method Does not support in mockafka
        self.consumer.committed(partitions=None)

    def test_get_watermark_offsets(self):
        # This method Does not support in mockafka
        self.consumer.get_watermark_offsets(partition=None)

    def test_offsets_for_times(self):
        # This method Does not support in mockafka
        self.consumer.offsets_for_times(partitions=None)

    def test_pause(self):
        # This method Does not support in mockafka
        self.consumer.pause(partitions=None)

    def test_position(self):
        # This method Does not support in mockafka
        self.consumer.position(partitions=None)

    def test_resume(self):
        # This method Does not support in mockafka
        self.consumer.resume(partitions=None)

    def test_seek(self):
        # This method Does not support in mockafka
        self.consumer.seek(partition=None)

    def test_store_offsets(self):
        # This method Does not support in mockafka
        self.consumer.store_offsets(message=None)

    def test_consumer_group_metadata(self):
        # This method Does not support in mockafka
        self.consumer.consumer_group_metadata()

    def test_incremental_assign(self):
        # This method Does not support in mockafka
        self.consumer.incremental_assign(partitions=None)

    def test_incremental_unassign(self):
        # This method Does not support in mockafka
        self.consumer.incremental_unassign(partitions=None)

    def test_message_timestamp_format(self):
        self.create_topic()
        self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])
        message = self.consumer.poll()

        # Fetch the timestamp from the message
        timestamp_type, timestamp = message.timestamp()

        # Expected timestamp types (matching confluent_kafka Message class)
        timestamp_create_time = 0
        timestamp_log_append_time = 1
        timestamp_not_available = 2

        # Test that the timestamp is returned as a tuple[int, int]
        self.assertIsInstance(timestamp, int)
        self.assertIsInstance(timestamp_type, int)
        self.assertIn(timestamp_type, [timestamp_create_time, timestamp_log_append_time, timestamp_not_available])

    def test_multiple_topics(self):
        """
        specifically testing a bug where if you are subscribe to more than 1 topic, and produce to poll() to just
        1 topic, at some point you will receive None for a message because of an extra random.shuffle in
        the FakeConsumer.poll() method.
        """

        self.create_topic()

        # create a second topic, but only produce to the first one
        second_topic = 'test_topic_2'
        self.kafka.create_partition(topic=second_topic, partitions=16)
        # because it's a random.shuffle, hopefully we trigger bad shuffle once in 30
        number_of_messages = 30
        # subscribe to both topics
        self.consumer.subscribe(topics=[self.test_topic, second_topic])
        for i in range(number_of_messages):
            self.producer.produce(
                topic=self.test_topic, partition=0, key=f"test{i}", value=f"test{i}"
            )

            message = self.consumer.poll()
            assert message is not None

from unittest import TestCase

import pytest

from mockafka.admin_client import FakeAdminClientImpl
from mockafka.conumser import FakeConsumer
from mockafka.kafka_store import KafkaStore, KafkaException
from mockafka.producer import FakeProducer


class TestFakeConsumer(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeProducer()
        self.consumer = FakeConsumer()
        self.admin = FakeAdminClientImpl()

    @pytest.fixture(autouse=True)
    def topic(self):
        self.test_topic = 'test_topic'

    def test_consume(self):
        self.test_poll()

    def test_close(self):
        pass

    def test_commit(self):
        pass

    def test_list_topics(self):
        pass

    def test_poll(self):
        pass

    def test_subscribe(self):
        test_topic_2 = 'test_topic_2'
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(
            self.consumer.subscribed_topic, topics
        )

    def test_subscribe_topic_not_exist(self):
        topics = [self.test_topic]
        with pytest.raises(KafkaException):
            self.consumer.subscribe(topics=topics)

    def test_unsubscribe(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(
            self.consumer.subscribed_topic, topics
        )
        self.consumer.unsubscribe(topics=topics)
        self.assertEqual(
            self.consumer.subscribed_topic, []
        )

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

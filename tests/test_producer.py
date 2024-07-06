from __future__ import annotations

from unittest import TestCase

import pytest

from mockafka.admin_client import FakeAdminClientImpl, NewTopic
from mockafka.kafka_store import KafkaStore, KafkaException
from mockafka.producer import FakeProducer
from confluent_kafka import Message  # type: ignore[import-untyped]


class TestFakeProducer(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeProducer()
        self.admin_client = FakeAdminClientImpl()

        # create topic with partitions
        self.admin_client.create_topics(
            topics=[
                NewTopic(topic="test1", num_partitions=4),
                NewTopic(topic="test2", num_partitions=8),
            ]
        )

    @pytest.fixture(autouse=True)
    def topic(self):
        self.topic = "test1"

    @pytest.fixture(autouse=True)
    def key(self):
        self.key = "test_key"

    @pytest.fixture(autouse=True)
    def value(self):
        self.value = "test_value"

    def test_produce_failed_topic_not_exist(self):
        with pytest.raises(KafkaException):
            self.producer.produce(
                headers={},
                key=self.key,
                value=self.value,
                topic="alaki",
                partition=0,
            )

    def test_produce_on_partition_not_exist(self):
        with pytest.raises(KafkaException):
            self.producer.produce(
                headers={},
                key=self.key,
                value=self.value,
                topic=self.topic,
                partition=17,
            )

    def test_produce_fail_for_none_partition(self):
        with pytest.raises(KafkaException):
            self.producer.produce(
                headers={},
                key=self.key,
                value=self.value,
                topic=self.topic,
                partition=None,
            )

    def test_produce_once(self):
        self.producer.produce(
            headers={},
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
        self.assertEqual(message.headers(), {})
        self.assertEqual(message.error(), None)
        self.assertEqual(message.latency(), None)

    def test_list_topics(self):
        cluster_metadata = self.producer.list_topics()
        self.assertEqual(len(cluster_metadata.topics.keys()), 2)
        self.assertEqual(len(cluster_metadata.topics["test1"]), 4)
        self.assertEqual(len(cluster_metadata.topics["test2"]), 8)

    def test_abort_transaction(self):
        # This method Does not support in mockafka
        self.producer.abort_transaction()

    def test_begin_transaction(self):
        # This method Does not support in mockafka
        self.producer.begin_transaction()

    def test_commit_transaction(self):
        # This method Does not support in mockafka
        self.producer.commit_transaction()

    def test_flush(self):
        # This method Does not support in mockafka
        self.producer.flush()

    def test_init_transactions(self):
        # This method Does not support in mockafka
        self.producer.init_transactions()

    def test_poll(self):
        # This method Does not support in mockafka
        self.producer.poll()

    def test_purge(self):
        # This method Does not support in mockafka
        self.producer.purge()

    def test_send_offsets_to_transaction(self):
        # This method Does not support in mockafka
        self.producer.send_offsets_to_transaction(positions=None, group_metadata=None)

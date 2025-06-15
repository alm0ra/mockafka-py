from __future__ import annotations

from unittest import TestCase

from mockafka.admin_client import FakeAdminClientImpl, NewPartitions, NewTopic
from mockafka.kafka_store import KafkaStore


class TestFakeAdminClient(TestCase):
    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.admin = FakeAdminClientImpl()
        self.test_partition = NewPartitions(topic="test", new_total_count=16)
        self.test_topic = NewTopic(topic="test", num_partitions=1)

    def test_create_partitions(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic from admin client
        self.admin.create_partitions([self.test_partition])

        # test there is not topic in mockafka
        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

        self.assertEqual(self.kafka.get_number_of_partition(topic="test"), 16)

    def test_create_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic via admin client
        self.admin.create_topics(topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

    def test_delete_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

        # create topic via admin client
        self.admin.create_topics(topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic="test"))

        # remove topic
        self.admin.delete_topics(topics=[self.test_topic])

        # test topic is removed from kafka
        self.assertFalse(self.kafka.is_topic_exist(topic="test"))

    def test_list_topics(self):
        self.admin.create_topics(
            topics=[
                NewTopic(topic="test1", num_partitions=1),
                NewTopic(topic="test2", num_partitions=4),
                NewTopic(topic="test3", num_partitions=16),
            ]
        )

        cluster_metadata = self.admin.list_topics()
        self.assertEqual(len(cluster_metadata.topics.keys()), 3)
        self.assertEqual(len(cluster_metadata.topics["test1"]), 1)
        self.assertEqual(len(cluster_metadata.topics["test2"]), 4)
        self.assertEqual(len(cluster_metadata.topics["test3"]), 16)

    def test_list_partitions(self):
        self.admin.create_topics(
            topics=[
                NewTopic(topic="test4", num_partitions=4),
            ]
        )

        cluster_metadata = self.admin.list_topics()
        topic_metadata = cluster_metadata.topics["test4"]
        self.assertEqual(len(topic_metadata.partitions), 4)
        self.assertEqual(topic_metadata.partitions[0].id, 0)
        self.assertEqual(len(topic_metadata.partitions[0].replicas), 1)

    def test_describe_acls(self):
        # This method Does not support in mockafka
        self.admin.describe_acls(acl_binding_filter=None, future=None)

    def test_describe_configs(self):
        # This method Does not support in mockafka
        self.admin.describe_configs(resources=None, future=None)

    def test_delete_acls(self):
        # This method Does not support in mockafka
        self.admin.delete_acls(acl_binding_filters=None, future=None)

    def test_alter_configs(self):
        # This method Does not support in mockafka
        self.admin.alter_configs()

    def test_create_acls(self):
        # This method Does not support in mockafka
        self.admin.create_acls()

    def test_list_groups(self):
        # This method Does not support in mockafka
        self.admin.list_groups()

    def test_poll(self):
        # This method Does not support in mockafka
        self.admin.poll()

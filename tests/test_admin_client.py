from unittest import TestCase
from mockafka.admin_client import FakeAdminClientImpl, NewPartitions, NewTopic
from mockafka.kafka_store import KafkaStore


class TestFakeAdminClient(TestCase):

    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.admin = FakeAdminClientImpl()
        self.test_partition = NewPartitions(topic='test', new_total_count=16)
        self.test_topic = NewTopic(topic='test', num_partitions=1)

    def test_create_partitions(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic='test'))

        # create topic from admin client
        self.admin.create_partitions([self.test_partition])

        # test there is not topic in mockafka
        self.assertTrue(self.kafka.is_topic_exist(topic='test'))

        self.assertEqual(self.kafka.get_number_of_partition(topic='test'), 16)

    def test_create_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic='test'))

        # create topic via admin client
        self.admin.create_topics(topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic='test'))

    def test_delete_topics(self):
        # test there is not topic in mockafka
        self.assertFalse(self.kafka.is_topic_exist(topic='test'))

        # create topic via admin client
        self.admin.create_topics(topics=[self.test_topic])

        self.assertTrue(self.kafka.is_topic_exist(topic='test'))

        # remove topic
        self.admin.delete_topics(topics=[self.test_topic])

        # test topic is removed from kafka
        self.assertFalse(self.kafka.is_topic_exist(topic='test'))

    def test_list_topics(self):
        self.admin.create_topics(topics=[
            NewTopic(topic='test1', num_partitions=1),
            NewTopic(topic='test2', num_partitions=4),
            NewTopic(topic='test3', num_partitions=16)
        ])

        cluster_metadata = self.admin.list_topics()
        self.assertEqual(len(cluster_metadata.topics.keys()), 3)
        self.assertEqual(
            len(cluster_metadata.topics['test1']), 1
        )
        self.assertEqual(
            len(cluster_metadata.topics['test2']), 4
        )
        self.assertEqual(
            len(cluster_metadata.topics['test3']), 16
        )


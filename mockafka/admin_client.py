from confluent_kafka.cimpl import NewTopic, NewPartitions

from mockafka import ClusterMetadata
from mockafka.kafka_store import KafkaStore

__all__ = ["FakeAdminClientImpl"]


class FakeAdminClientImpl:
    """
    Kafka Fake Admin Client

    .. py:function:: Admin(**kwargs)

      Create a new AdminClient instance using the provided configuration dict.

    This class should not be used directly, use confluent_kafka.AdminClient
    .
    .. py:function:: len()

      :returns: Number Kafka protocol requests waiting to be delivered to, or returned from, broker.
      :rtype: int
    """

    def __init__(self, *args, **kwargs):
        self.kafka = KafkaStore()

    def create_partitions(self, partitions: list[NewPartitions]):
        for partition in partitions:
            self.create_partition(partition)

    def create_partition(self, partition: NewPartitions):
        self.kafka.create_partition(topic=partition.topic, partitions=partition.new_total_count)

    def create_topics(self, topics: list[NewTopic]):
        for topic in topics:
            self.create_topic(topic=topic)

    def create_topic(self, topic: NewTopic):
        self.kafka.create_topic(topic.topic)
        self.create_partitions([NewPartitions(topic.topic, topic.num_partitions)])

    def delete_topics(self, topics, future, request_timeout=None,
                      operation_timeout=None):
        for topic in topics:
            self.delete_topic(topic=topic)

    def delete_topic(self, topic: NewTopic):
        self.kafka.remove_topic(topic=topic.topic)

    def describe_acls(self, acl_binding_filter, future,
                      request_timeout=None):
        # This method Does not support in mockafka
        pass

    def describe_configs(self, resources, future, request_timeout=None,
                         broker=None):
        # This method Does not support in mockafka
        pass

    def delete_acls(self, acl_binding_filters, future,
                    request_timeout=None):
        # This method Does not support in mockafka
        pass

    def alter_configs(self, *args, **kwargs):
        # This method Does not support in mockafka
        pass

    def create_acls(self, *args, **kwargs):
        # This method Does not support in mockafka
        pass

    def list_groups(self, group=None, *args,
                    **kwargs):
        # This method Does not support in mockafka
        pass

    def list_topics(self, topic=None, *args,
                    **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
        return ClusterMetadata(topic)

    def poll(self, timeout=None):
        # This method Does not support in mockafka
        pass

    def __len__(self, *args, **kwargs):
        pass

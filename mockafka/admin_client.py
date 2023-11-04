from confluent_kafka.admin import TopicMetadata
from .store import mock_topics, offset_store
from confluent_kafka.cimpl import NewTopic

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

    def create_partitions(self, partitions: list[NewPartitions]):
        for partition in partitions:
            self.create_partition(partition)

    def create_partition(self, partition: NewPartitions):
        topic = partition.topic
        partition_count = partition.new_total_count

        if topic in mock_topics.keys():
            # Increase number of partitions
            len_of_current_partition = len(mock_topics[topic].keys())
            if partition_count > len_of_current_partition:
                for i in range(len_of_current_partition, partition_count):
                    mock_topics[topic][i] = []
                    offset_store[f'{topic}-{i}'] = {
                        'first_offset': 0,
                        'next_offset': 0
                    }
            elif partipartition_counttion == len_of_current_partition:
                pass

            else:
                raise Exception(f"{topic} Can not Decrease partition topic.")

    def create_topics(self, topics: list[NewTopic]):
        for topic in topics:
            self.create_topic(topic=topic)

    def create_topic(self, topic: NewTopic):
        if topic.topic in mock_topics.keys():
            raise Exception(f'{topic.topic} Topic already exist')

        # create topic
        mock_topics[topic] = {}

        self.create_partition([NewPartitions(topic.topic, topic.num_partitions)])

    def delete_topics(self, topics, future, request_timeout=None,
                      operation_timeout=None):
        for topic in topics:
            self.delete_topic(topic=topic)

    def delete_topic(self, topic: NewTopic):
        if topic.topic not in mock_topics.keys():
            raise Exception("Topic Does not exist")
        mock_topics.pop(topic.topic)
        for offset in offset_store:
            if topic in offset:
                offset_store.pop(offset)

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

    def __init__(self, *args, **kwargs):
        pass

    def __len__(self, *args, **kwargs):
        pass


class ClusterMetadata(object):
    """
    Provides information about the Kafka cluster, brokers, and topics.
    Returned by list_topics().

    This class is typically not user instantiated.
    """

    def __init__(self, topic):
        self.cluster_id = 'eAvlnr_4QISNbc5bIwBRVA'
        self.controller_id = 1
        self.brokers = {1: FakeBrokerMetadata()}
        self.topics = {}
        if topic in mock_topics.keys():
            self.topics[topic] = TopicMetadata(topic, len(mock_topics[topic].keys()))
        self.orig_broker_id = -1
        self.orig_broker_name = None

    def __repr__(self):
        return "ClusterMetadata({})".format(self.cluster_id)

    def __str__(self):
        return str(self.cluster_id)


class FakeBrokerMetadata(object):
    """
    Provides information about a Kafka broker.

    This class is typically not user instantiated.
    """

    def __init__(self):
        self.id = 1
        """Broker id"""
        self.host = 'fakebroker'
        """Broker hostname"""
        self.port = 9091
        """Broker port"""

    def __repr__(self):
        return "BrokerMetadata({}, {}:{})".format(self.id, self.host, self.port)

    def __str__(self):
        return "{}:{}/{}".format(self.host, self.port, self.id)


class TopicMetadata(object):
    """
    Provides information about a Kafka topic.

    This class is typically not user instantiated.
    """

    # The dash in "-topic" and "-error" is needed to circumvent a
    # Sphinx issue where it tries to reference the same instance variable
    # on other classes which raises a warning/error.

    def __init__(self, topic_name, partition_num: int = 4):
        self.topic = topic_name
        """Topic name"""
        self.partitions = partition_num
        """Map of partitions indexed by partition id. Value is a PartitionMetadata object."""
        self.error = None
        """Topic error, or None. Value is a KafkaError object."""

    def __repr__(self):
        if self.error is not None:
            return "TopicMetadata({}, {} partitions, {})".format(self.topic, len(self.partitions), self.error)
        else:
            return "TopicMetadata({}, {} partitions)".format(self.topic, len(self.partitions))

    def __str__(self):
        return self.topic

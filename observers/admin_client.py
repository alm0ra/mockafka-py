from confluent_kafka.admin import TopicMetadata

__all__ = ["FakeAdminClientImpl"]

kafka_topics = dict[str, dict[int, list]]


class FakeAdminClientImpl:
    """
    Kafka Admin Client

    .. py:function:: Admin(**kwargs)

      Create a new AdminClient instance using the provided configuration dict.

    This class should not be used directly, use confluent_kafka.AdminClient
    .
    .. py:function:: len()

      :returns: Number Kafka protocol requests waiting to be delivered to, or returned from, broker.
      :rtype: int
    """

    def __init__(self, *args, **kwargs):
        pass

    def __len__(self, *args, **kwargs):
        pass

    def create_partitions(self, *args, **kwargs):  # real signature unknown; restored from __doc__
        pass

    def create_topics(self, topics, *args, **kwargs):  # real signature unknown; restored from __doc__
        for topic in topics:
            if topic in kafka_topics.keys():
                continue
            kafka_topics[topic] = []


    def delete_topics(self, topics, future, request_timeout=None,
                      operation_timeout=None):  # real signature unknown; restored from __doc__
        for topic in topics:
            if topic in kafka_topics.keys():
                kafka_topics.pop(topic)

    def list_groups(self, group=None, *args,
                    **kwargs):
        pass

    def list_topics(self, topic=None, *args,
                    **kwargs):
        return list(kafka_topics.keys())
        # return ClusterMetadata(topic)

    def poll(self, timeout=None):
        pass

    def describe_acls(self, acl_binding_filter, future,
                      request_timeout=None):
        # This method is not supported by mockafka
        pass

    def create_acls(self, *args, **kwargs):
        # This method is not supported by mockafka
        pass

    def delete_acls(self, acl_binding_filters, future,
                    request_timeout=None):
        # This method is not supported by mockafka
        pass

    def alter_configs(self, *args, **kwargs):
        # This method is not supported by mockafka
        pass

    def describe_configs(self, resources, future, request_timeout=None,
                         broker=None):
        # This method is not supported by mockafka
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
        self.topics = {topic: TopicMetadata(topic)}
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

    def __init__(self, topic_name):
        self.topic = topic_name
        """Topic name"""
        self.partitions = range(32)
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

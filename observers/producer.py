__all__ = ["FakeProducer"]


class FakeProducer(object):
    """
    Asynchronous Fake Kafka Producer

    .. py:function:: Producer(config)

      :param dict config: Configuration properties. At a minimum ``bootstrap.servers`` **should** be set

      Create a new Producer instance using the provided configuration dict.


    .. py:function:: __len__(self)

      Producer implements __len__ that can be used as len(producer) to obtain number of messages waiting.
      :returns: Number of messages and Kafka protocol requests waiting to be delivered to broker.
      :rtype: int
    """

    def __init__(self, config):
        pass

    def __len__(self, *args, **kwargs):
        pass

    def abort_transaction(self, timeout=None):
        # This method is not supported by mockafka
        pass

    def begin_transaction(self):
        # This method is not supported by mockafka
        pass

    def commit_transaction(self, timeout=None):
        # This method is not supported by mockafka
        pass

    def flush(self, timeout=None):
        # This method is not supported by mockafka
        return 0

    def init_transactions(self, timeout=None):
        # This method is not supported by mockafka
        pass

    def list_topics(self, topic=None, *args,
                    **kwargs):
        return ClusterMetadata(topic)

    def poll(self, timeout=None):
        return 0

    def produce(self, topic, value=None, *args, **kwargs):
        return None

    def purge(self, in_queue=True, *args, **kwargs):
        pass

    def send_offsets_to_transaction(self, positions, group_metadata,
                                    timeout=None):
        # This method is not supported by mockafka
        pass


class ClusterMetadata(object):
    """
    Provides information about the Kafka cluster, brokers, and topics.
    Returned by list_topics().

    This class is typically not user instantiated.
    """

    def __init__(self, topic):
        self.cluster_id = None
        self.controller_id = -1
        self.brokers = {}
        self.topics = {'name': topic}
        self.orig_broker_id = -1
        self.orig_broker_name = None

    def __repr__(self):
        return "ClusterMetadata({})".format(self.cluster_id)

    def __str__(self):
        return str(self.cluster_id)


class TopicPartition(object):
    """
    TopicPartition is a generic type to hold a single partition and various information about it.

    It is typically used to provide a list of topics or partitions for various operations, such as :py:func:`Consumer.assign()`.

    .. py:function:: TopicPartition(topic, [partition], [offset])

      Instantiate a TopicPartition object.

      :param string topic: Topic name
      :param int partition: Partition id
      :param int offset: Initial partition offset
      :rtype: TopicPartition
    """

    def __eq__(self, *args, **kwargs):
        pass

    def __getattribute__(self, *args, **kwargs):
        pass

    def __ge__(self, *args, **kwargs):
        pass

    def __gt__(self, *args, **kwargs):
        pass

    def __hash__(self, *args, **kwargs):
        pass

    def __init__(self, topic, partition=None, *args,
                 **kwargs):
        pass

    def __le__(self, *args, **kwargs):
        pass

    def __lt__(self, *args, **kwargs):
        pass

    @staticmethod
    def __new__(*args, **kwargs):
        pass

    def __ne__(self, *args, **kwargs):
        pass

    def __repr__(self, *args, **kwargs):
        pass

    error = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    offset = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    partition = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    topic = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

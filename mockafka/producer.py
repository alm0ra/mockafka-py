from mockafka.cluster_metadata import ClusterMetadata
from mockafka.kafka_store import KafkaStore
from mockafka.message import Message

__all__ = ["FakeProducer"]


class FakeProducer(object):
    def __init__(self, config):
        self.kafka = KafkaStore()

    def produce(self, topic, value=None, *args, **kwargs):
        # create a message and call produce kafka
        message = Message(value=value, *args, **kwargs)
        self.kafka.produce(message=message, topic=topic, partition=kwargs['partition'])

    def list_topics(self, topic=None, *args, **kwargs):
        return ClusterMetadata(topic)

    def abort_transaction(self, timeout=None):
        # This method Does not support in mockafka
        pass

    def begin_transaction(self):
        # This method Does not support in mockafka
        pass

    def commit_transaction(self, timeout=None):
        # This method Does not support in mockafka
        pass

    def flush(self, timeout=None):
        # This method Does not support in mockafka
        return 0

    def init_transactions(self, timeout=None):
        # This method Does not support in mockafka
        pass

    def poll(self, timeout=None):
        # This method Does not support in mockafka
        return 0

    def purge(self, in_queue=True, *args, **kwargs):
        # This method Does not support in mockafka
        pass

    def send_offsets_to_transaction(self, positions, group_metadata,
                                    timeout=None):
        # This method Does not support in mockafka
        pass

    def __len__(self, *args, **kwargs):
        # This method Does not support in mockafka
        pass


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

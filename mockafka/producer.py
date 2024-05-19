from __future__ import annotations

from mockafka.cluster_metadata import ClusterMetadata
from mockafka.kafka_store import KafkaStore
from mockafka.message import Message

__all__ = ["FakeProducer"]


class FakeProducer(object):
    def __init__(self, config: dict = None):
        self.kafka = KafkaStore()

    def produce(self, topic, value=None, *args, **kwargs):
        # create a message and call produce kafka
        message = Message(value=value, topic=topic, *args, **kwargs)
        self.kafka.produce(message=message, topic=topic, partition=kwargs["partition"])

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

    def send_offsets_to_transaction(self, positions, group_metadata, timeout=None):
        # This method Does not support in mockafka
        pass

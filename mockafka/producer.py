from __future__ import annotations

from typing import Optional, Union

from mockafka.cluster_metadata import ClusterMetadata
from mockafka.kafka_store import KafkaStore
from mockafka.message import Message

__all__ = ["FakeProducer"]


class FakeProducer(object):
    def __init__(self, config: dict | None = None):
        self.kafka = KafkaStore()

    def produce(
        self,
        topic,
        value=None,
        key=None,
        partition=None,
        callback=None,
        on_delivery=None,
        timestamp=None,
        headers: Union[
            # While Kafka itself supports only list[tuple[...]], confluent_kafka
            # allows passing in a dict here.
            dict[str, Optional[bytes]],
            list[tuple[str, Optional[bytes]]],
            None,
        ] = None,
        **kwargs,
    ) -> None:
        if isinstance(headers, dict):
            headers = list(headers.items())
        # create a message and call produce kafka
        message = Message(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            callback=callback,
            on_delivery=on_delivery,
            timestamp=timestamp,
            headers=headers,
            **kwargs,
        )
        self.kafka.produce(message=message, topic=topic, partition=partition)

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

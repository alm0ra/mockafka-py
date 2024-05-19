from __future__ import annotations

import logging
from mockafka.broker_metadata import BrokerMetadata
from mockafka.kafka_store import KafkaStore
from mockafka.topic_metadata import TopicMetadata


class ClusterMetadata(object):
    """
    Provides information about the Kafka cluster, brokers, and topics.
    Returned by list_topics().

    This class is typically not user instantiated.
    """

    def __init__(self, topic: str = None):
        self.kafka = KafkaStore()
        self.cluster_id = "test"
        self.controller_id = 1
        self.brokers = {1: BrokerMetadata()}
        self.topics = CustomDict()
        if topic:
            if self.kafka.is_topic_exist(topic=topic):
                self.topics[topic] = TopicMetadata(
                    topic, self.kafka.partition_list(topic=topic)
                )

        else:
            for topic in self.kafka.topic_list():
                self.topics[topic] = TopicMetadata(
                    topic, self.kafka.partition_list(topic=topic)
                )

        self.orig_broker_id = -1
        self.orig_broker_name = None

    def __repr__(self):
        return "ClusterMetadata({})".format(self.cluster_id)

    def __str__(self):
        return str(self.cluster_id)


class CustomDict(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            logging.warning(f"Key '{key}' not found in CustomDict")
            return

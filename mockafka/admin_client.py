from __future__ import annotations

from confluent_kafka.cimpl import NewTopic, NewPartitions

from mockafka.cluster_metadata import ClusterMetadata
from mockafka.kafka_store import KafkaStore

__all__ = ["FakeAdminClientImpl"]


class FakeAdminClientImpl:
    """
    Mock implementation of the Confluent Kafka AdminClient for testing purposes.

    Attributes:
    - kafka (KafkaStore): The in-memory storage for simulating Kafka behavior.
    - clean (bool): Flag indicating whether to start with a clean slate.

    Methods: - create_partitions(partitions: List[NewPartitions]): Create partitions in the in-memory Kafka store. -
    create_partition(partition: NewPartitions): Create a single partition in the in-memory Kafka store. -
    create_topics(topics: List[NewTopic]): Create topics in the in-memory Kafka store. - create_topic(topic:
    NewTopic): Create a single topic in the in-memory Kafka store. - delete_topics(topics, future=None,
    request_timeout=None, operation_timeout=None): Delete topics from the in-memory Kafka store. - delete_topic(
    topic: NewTopic): Delete a single topic from the in-memory Kafka store. - describe_acls(acl_binding_filter,
    future, request_timeout=None): Describe ACLs (unsupported in mockafka). - describe_configs(resources, future,
    request_timeout=None, broker=None): Describe configurations (unsupported in mockafka). - delete_acls(
    acl_binding_filters, future, request_timeout=None): Delete ACLs (unsupported in mockafka). - alter_configs(*args,
    **kwargs): Alter configurations (unsupported in mockafka). - create_acls(*args, **kwargs): Create ACLs (
    unsupported in mockafka). - list_groups(group=None, *args, **kwargs): List consumer groups (unsupported in
    mockafka). - list_topics(topic=None, *args, **kwargs): List topics (returns ClusterMetadata). - poll(
    timeout=None): Poll for events (unsupported in mockafka). - __len__(*args, **kwargs): Get the length of the Kafka
    store (not implemented).
    """

    def __init__(self, clean: bool = False, *args, **kwargs):
        """
        Initialize the FakeAdminClientImpl.

        Parameters:
        - clean (bool): Flag indicating whether to start with a clean slate.
        """
        self.kafka = KafkaStore(clean=clean)

    def create_partitions(self, partitions: list[NewPartitions]):
        """
        Create partitions in the in-memory Kafka store.

        Parameters:
        - partitions (List[NewPartitions]): List of partition objects to be created.
        """
        for partition in partitions:
            self.create_partition(partition)

    def create_partition(self, partition: NewPartitions):
        """
        Create a single partition in the in-memory Kafka store.

        Parameters:
        - partition (NewPartitions): The partition object to be created.
        """
        self.kafka.create_partition(
            topic=partition.topic, partitions=partition.new_total_count
        )

    def create_topics(self, topics: list[NewTopic]):
        """
        Create topics in the in-memory Kafka store.

        Parameters:
        - topics (List[NewTopic]): List of topic objects to be created.
        """
        for topic in topics:
            self.create_topic(topic=topic)

    def create_topic(self, topic: NewTopic):
        """
        Create a single topic in the in-memory Kafka store.

        Parameters:
        - topic (NewTopic): The topic object to be created.
        """
        self.kafka.create_topic(topic.topic)
        self.create_partitions([NewPartitions(topic.topic, topic.num_partitions)])

    def delete_topics(
        self, topics, future=None, request_timeout=None, operation_timeout=None
    ):
        """
        Delete topics from the in-memory Kafka store.

        Parameters:
        - topics: Topics to be deleted.
        - future: Unused parameter (for compatibility).
        - request_timeout: Unused parameter (for compatibility).
        - operation_timeout: Unused parameter (for compatibility).
        """
        for topic in topics:
            self.delete_topic(topic=topic)

    def delete_topic(self, topic: NewTopic):
        """
        Delete a single topic from the in-memory Kafka store.

        Parameters:
        - topic (NewTopic): The topic object to be deleted.
        """
        self.kafka.remove_topic(topic=topic.topic)

    def describe_acls(self, acl_binding_filter, future, request_timeout=None):
        """
        Describe ACLs (unsupported in mockafka).

        Parameters:
        - acl_binding_filter: Unused parameter (unsupported).
        - future: Unused parameter (unsupported).
        - request_timeout: Unused parameter (unsupported).
        """
        pass

    def describe_configs(self, resources, future, request_timeout=None, broker=None):
        """
        Describe configurations (unsupported in mockafka).

        Parameters:
        - resources: Unused parameter (unsupported).
        - future: Unused parameter (unsupported).
        - request_timeout: Unused parameter (unsupported).
        - broker: Unused parameter (unsupported).
        """
        pass

    def delete_acls(self, acl_binding_filters, future, request_timeout=None):
        """
        Delete ACLs (unsupported in mockafka).

        Parameters:
        - acl_binding_filters: Unused parameter (unsupported).
        - future: Unused parameter (unsupported).
        - request_timeout: Unused parameter (unsupported).
        """
        pass

    def alter_configs(self, *args, **kwargs):
        """
        Alter configurations (unsupported in mockafka).

        Parameters:
        - args: Unused parameter (unsupported).
        - kwargs: Unused parameter (unsupported).
        """
        pass

    def create_acls(self, *args, **kwargs):
        """
        Create ACLs (unsupported in mockafka).

        Parameters:
        - args: Unused parameter (unsupported).
        - kwargs: Unused parameter (unsupported).
        """
        pass

    def list_groups(self, group=None, *args, **kwargs):
        """
        List consumer groups (unsupported in mockafka).

        Parameters:
        - group: Unused parameter (unsupported).
        - args: Unused parameter (unsupported).
        - kwargs: Unused parameter (unsupported).
        """
        pass

    def list_topics(self, topic=None, *args, **kwargs):
        """
        List topics (returns ClusterMetadata).

        Parameters:
        - topic: Unused parameter (for compatibility).
        - args: Unused parameter (for compatibility).
        - kwargs: Unused parameter (for compatibility).

        Returns:
        - ClusterMetadata: Metadata of the listed topics.
        """
        return ClusterMetadata(topic)

    def poll(self, timeout=None):
        """
        Poll for events (unsupported in mockafka).

        Parameters:
        - timeout: Unused parameter (unsupported).
        """
        pass

    def __len__(self, *args, **kwargs):
        """
        Get the length of the Kafka store (not implemented).

        Parameters:
        - args: Unused parameters (not implemented).
        - kwargs: Unused parameters (not implemented).
        """
        pass

from __future__ import annotations


class TopicMetadata(object):
    """
    Provides information about a Kafka topic.

    This class is typically not user instantiated.
    """

    # The dash in "-topic" and "-error" is needed to circumvent a
    # Sphinx issue where it tries to reference the same instance variable
    # on other classes which raises a warning/error.

    def __init__(self, topic_name: str, partition_num: list = []):
        self.topic = topic_name
        """Topic name"""
        self.partitions = partition_num
        """Map of partitions indexed by partition id. Value is a PartitionMetadata object."""
        self.error = None
        """Topic error, or None. Value is a KafkaError object."""

    def __str__(self):
        return self.topic

    def __len__(self):
        return len(self.partitions)

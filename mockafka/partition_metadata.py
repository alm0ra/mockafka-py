from __future__ import annotations

from confluent_kafka import (  # type: ignore[import-untyped]
    KafkaError,
)

class PartitionMetadata(object):
    """
    Provides information about a Kafka partition.

    This class is typically not user instantiated.
    """

    # The dash in "-topic" and "-error" is needed to circumvent a
    # Sphinx issue where it tries to reference the same instance variable
    # on other classes which raises a warning/error.

    def __init__(self, id: int, leader: int = -1, replicas: list[int] | None = None, isrs: list[int] | None = None, error: KafkaError | None = None):
        self.id = id
        """Partition Id"""
        self.leader = leader
        """Current leader broker for this partition, or -1."""
        self.replicas = replicas or []
        """List of replica broker ids for this partition."""
        self.isrs = isrs or []
        """List of in-sync-replica broker ids for this partition."""
        self.error = error
        """Partition error, or None. Value is a KafkaError object."""
        
        # If default args were provided then initialize the Partition with a single replica
        if leader == -1 and replicas is None and isrs is None:
            self.leader = 1
            self.replicas = [1]
            self.isrs = [1]
            
    def __str__(self):
        return self.id

    def __len__(self):
        return len(self.replicas)

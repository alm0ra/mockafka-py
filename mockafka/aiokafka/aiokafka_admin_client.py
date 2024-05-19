from __future__ import annotations

from typing import Dict

from aiokafka.admin import NewTopic, NewPartitions

from mockafka.kafka_store import KafkaStore


class FakeAIOKafkaAdmin:
    """
    FakeAIOKafkaAdmin is a mock implementation of aiokafka's AIOKafkaAdminClient.

    Parameters:
    - clean (bool): Whether to clean/reset the underlying KafkaStore on init. Default False.

    Methods:
    - close(): Close the admin client.
    - start(): Start the admin client.
    - _create_topic(): Create a topic in the underlying KafkaStore.
      Takes the NewTopic object containing name and num_partitions.
    - _remove_topic(): Delete a topic from the underlying KafkaStore by name.
    - create_topics(): Create multiple topics from a list of NewTopic objects.
      Calls _create_topic() for each one.
    - delete_topics(): Delete multiple topics by name from a list of strings.
      Calls _remove_topic() for each one.
    - _create_partition(): Add partitions to a topic in KafkaStore.
      Takes the topic name and number of partitions to add.
    - create_partitions(): Add partitions to multiple topics from a dict mapping
      topic name to NewPartitions object containing total_count.
      Calls _create_partition() for each topic.
    """

    def __init__(self, clean: bool = False, *args, **kwargs):
        self.kafka = KafkaStore(clean=clean)

    async def close(self):
        pass

    async def start(self):
        pass

    async def _create_topic(self, topic: NewTopic) -> None:
        self.kafka.create_topic(topic.name)
        await self._create_partition(
            topic=topic.name, partition_count=topic.num_partitions
        )

    async def _remove_topic(self, topic: str):
        self.kafka.remove_topic(topic=topic)

    async def create_topics(self, new_topics: list[NewTopic], *args, **kwargs):
        for topic in new_topics:
            await self._create_topic(topic=topic)

    async def delete_topics(self, topics: list[str], **kwargs) -> None:
        for topic in topics:
            await self._remove_topic(topic=topic)

    async def _create_partition(self, topic: str, partition_count: int):
        self.kafka.create_partition(topic=topic, partitions=partition_count)

    async def create_partitions(
        self, topic_partitions: Dict[str, NewPartitions], *args, **kwargs
    ):
        for topic, partition in topic_partitions.items():
            await self._create_partition(
                topic=topic, partition_count=partition.total_count
            )

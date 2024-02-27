from typing import Dict
from asyncio import create_task
from aiokafka.admin import NewTopic, NewPartitions

from mockafka.kafka_store import KafkaStore


class FakeAIOKafkaAdmin:
    def __init__(self, clean: bool = False, *args, **kwargs):
        self.kafka = KafkaStore(clean=clean)

    async def close(self):
        pass

    async def start(self):
        pass

    async def _create_topic(self, topic: NewTopic) -> None:
        self.kafka.create_topic(topic.name)
        await self._create_partition(topic=topic.name, partition_count=topic.num_partitions)

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

    async def create_partitions(self, topic_partitions: Dict[str, NewPartitions], *args, **kwargs):
        for topic, partition in topic_partitions.items():
            await self._create_partition(topic=topic, partition_count=partition.total_count)

from __future__ import annotations

import random
from copy import deepcopy

from mockafka.kafka_store import KafkaStore


class FakeAIOKafkaConsumer:
    """
    FakeAIOKafkaConsumer is a mock implementation of aiokafka's AIOKafkaConsumer.

    It allows mocking a kafka consumer for testing purposes.

    Parameters:
    - args, kwargs: Passed to superclass init, not used here.

    Attributes:
    - kafka: KafkaStore instance for underlying storage.
    - consumer_store (dict): Tracks consumption progress per topic/partition.
    - subscribed_topic (list): List of subscribed topic names.

    Methods:
    - start(): Reset internal state.
    - stop(): Reset internal state.
    - commit(): Commit offsets to KafkaStore by updating first_offset.
    - topics(): Get subscribed topics.
    - subscribe(): Subscribe to topics by name.
    - subscription(): Get subscribed topics.
    - unsubscribe(): Reset subscribed topics.
    - _get_key(): Generate consumer_store lookup key from topic/partition.
    - getone(): Get next available message from subscribed topics.
      Updates consumer_store as messages are consumed.
    - getmany(): Currently just calls getone().
    """

    def __init__(self, *args, **kwargs):
        self.kafka = KafkaStore()
        self.consumer_store = {}
        self.subscribed_topic: list = []

    async def start(self):
        self.consumer_store = {}
        self.subscribed_topic: list = []

    async def stop(self):
        self.consumer_store = {}
        self.subscribed_topic: list = []

    async def commit(self):
        for item in self.consumer_store:
            topic, partition = item.split("*")
            if (
                self.kafka.get_partition_first_offset(topic, partition)
                <= self.consumer_store[item]
            ):
                self.kafka.set_first_offset(
                    topic=topic, partition=partition, value=self.consumer_store[item]
                )

        self.consumer_store = {}

    async def topics(self):
        return self.subscribed_topic

    def subscribe(self, topics: list[str]):
        for topic in topics:
            if not self.kafka.is_topic_exist(topic):
                continue

            if topic not in self.subscribed_topic:
                self.subscribed_topic.append(topic)

    def subscribtion(self) -> list[str]:
        return self.subscribed_topic

    def unsubscribe(self):
        self.subscribed_topic = []

    def _get_key(self, topic, partition) -> str:
        return f"{topic}*{partition}"

    async def getone(self):
        topics_to_consume = deepcopy(self.subscribed_topic)
        random.shuffle(topics_to_consume)

        for topic in topics_to_consume:
            partition_to_consume = deepcopy(self.kafka.partition_list(topic=topic))
            random.shuffle(topics_to_consume)

            for partition in partition_to_consume:
                first_offset = self.kafka.get_partition_first_offset(
                    topic=topic, partition=partition
                )
                next_offset = self.kafka.get_partition_next_offset(
                    topic=topic, partition=partition
                )
                consumer_amount = self.consumer_store.get(
                    self._get_key(topic, partition)
                )
                if first_offset == next_offset:
                    continue

                if consumer_amount == next_offset:
                    continue

                if consumer_amount is not None:
                    self.consumer_store[self._get_key(topic, partition)] += 1
                else:
                    self.consumer_store[self._get_key(topic, partition)] = (
                        first_offset + 1
                    )

                return self.kafka.get_message(
                    topic=topic, partition=partition, offset=first_offset
                )

        return None

    async def getmany(self):
        # FIXME: must impelement
        return await self.getone()

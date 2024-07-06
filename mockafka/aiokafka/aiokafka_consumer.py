from __future__ import annotations

import random
import re
import warnings
from typing import Any

from aiokafka.abc import ConsumerRebalanceListener  # type: ignore[import-untyped]
from aiokafka.structs import TopicPartition  # type: ignore[import-untyped]

from mockafka.kafka_store import KafkaStore
from mockafka.message import Message


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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.kafka = KafkaStore()
        self.consumer_store: dict[str, int] = {}
        self.subscribed_topic: list = []

    async def start(self) -> None:
        self.consumer_store = {}
        self.subscribed_topic = []

    async def stop(self) -> None:
        self.consumer_store = {}
        self.subscribed_topic = []

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

    def subscribe(
        self,
        topics: list[str] | set[str] | tuple[str, ...] = (),
        pattern: str | None = None,
        listener: ConsumerRebalanceListener | None = None,
    ) -> None:
        if topics and pattern:
            raise ValueError(
                "Only one of `topics` and `pattern` may be provided (not both).",
            )
        if not topics and not pattern:
            raise ValueError(
                "Must provide one of `topics` and `pattern`.",
            )

        if listener:
            warnings.warn(
                "`listener` is not implemented.",
                stacklevel=2,
            )

        if pattern:
            assert not topics
            warnings.warn(
                "`pattern` only support topics which exist at the time of subscription.",
                stacklevel=2,
            )
            topics = [x for x in self.kafka.topic_list() if re.match(pattern, x)]

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

    async def getone(self, *partitions: TopicPartition) -> Message:
        if partitions:
            partitions_to_consume = list(partitions)
        else:
            partitions_to_consume = [
                TopicPartition(x, y)
                for x in self.subscribed_topic
                for y in self.kafka.partition_list(topic=x)
            ]

        random.shuffle(partitions_to_consume)

        for topic, partition in partitions_to_consume:
            first_offset = self.kafka.get_partition_first_offset(
                topic=topic, partition=partition
            )
            next_offset = self.kafka.get_partition_next_offset(
                topic=topic, partition=partition
            )
            if first_offset == next_offset:
                # Topic partition is empty
                continue

            topic_key = self._get_key(topic, partition)

            consumer_amount = self.consumer_store.setdefault(topic_key, first_offset)
            if consumer_amount == next_offset:
                # Topic partition is exhausted
                continue

            self.consumer_store[topic_key] += 1

            return self.kafka.get_message(
                topic=topic, partition=partition, offset=consumer_amount
            )

        return None

    async def getmany(self):
        # FIXME: must impelement
        return await self.getone()

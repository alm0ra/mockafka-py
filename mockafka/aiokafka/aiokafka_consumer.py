from __future__ import annotations

import collections
import itertools
import random
import re
import warnings
from collections.abc import Iterable, Iterator, Set
from typing import Any, Optional

from aiokafka.abc import ConsumerRebalanceListener  # type: ignore[import-untyped]
from aiokafka.errors import ConsumerStoppedError  # type: ignore[import-untyped]
from aiokafka.structs import (  # type: ignore[import-untyped]
    ConsumerRecord,
    TopicPartition,
)

from mockafka.kafka_store import KafkaStore
from mockafka.message import Message


def message_to_record(message: Message, offset: int) -> ConsumerRecord[bytes, bytes]:
    topic: Optional[str] = message.topic()
    partition: Optional[int] = message.partition()
    _, timestamp = message.timestamp()

    if topic is None or partition is None or timestamp is None:
        fields = [
            ("topic", topic),
            ("partition", partition),
            ("timestamp", timestamp),
        ]
        missing = ", ".join(x for x, y in fields if y is None)
        raise ValueError(f"Message is missing key components: {missing}")

    key_str: Optional[str] = message.key()
    value_str: Optional[str] = message.value()

    key = key_str.encode() if key_str is not None else None
    value = value_str.encode() if value_str is not None else None

    return ConsumerRecord(
        topic=topic,
        partition=partition,
        offset=offset,
        timestamp=timestamp,
        # https://github.com/apache/kafka/blob/932759bd70ce646ced5298a2ad8db02c0cea3643/clients/src/main/java/org/apache/kafka/common/record/TimestampType.java#L25
        timestamp_type=0,  # CreateTime
        key=key,
        value=value,
        checksum=None,  # Deprecated, we won't support it
        serialized_key_size=len(key) if key else 0,
        serialized_value_size=len(value) if value else 0,
        headers=tuple((message.headers() or {}).items()),
    )


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
    - getmany(): Get next available messages from subscribed topics.
      Updates consumer_store as messages are consumed.
    """

    def __init__(self, *topics: str, **kwargs: Any) -> None:
        self.kafka = KafkaStore()
        self.consumer_store: dict[str, int] = {}
        self.subscribed_topic = [x for x in topics if self.kafka.is_topic_exist(x)]
        self._is_closed = True

    async def start(self) -> None:
        self.consumer_store = {}
        self._is_closed = False

    async def stop(self) -> None:
        self.consumer_store = {}
        self._is_closed = True

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

    async def topics(self) -> set[str]:
        return set(self.kafka.topic_list())

    def subscribe(
            self,
            topics: list[str] | set[str] | tuple[str, ...] = (),
            pattern: str | None = None,
            listener: Optional[ConsumerRebalanceListener] = None,
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

    # AIOKafkaConsumer.subscription returns a `frozenset` most of the time but
    # can also return an empty `set` in some cases. Reflect that in our type
    # annotation even though we only ever return one type.
    def subscription(self) -> Set[str]:
        return frozenset(self.subscribed_topic)

    def unsubscribe(self) -> None:
        self.subscribed_topic = []

    def _get_key(self, topic, partition) -> str:
        return f"{topic}*{partition}"

    def _fetch_one(self, topic: str, partition: int) -> Optional[ConsumerRecord[bytes, bytes]]:

        first_offset = self.kafka.get_partition_first_offset(
            topic=topic, partition=partition
        )
        next_offset = self.kafka.get_partition_next_offset(
            topic=topic, partition=partition
        )
        if first_offset == next_offset:
            # Topic partition is empty
            return None

        topic_key = self._get_key(topic, partition)

        consumer_amount = self.consumer_store.setdefault(topic_key, first_offset)
        if consumer_amount == next_offset:
            # Topic partition is exhausted
            return None

        self.consumer_store[topic_key] += 1

        message = self.kafka.get_message(
            topic=topic, partition=partition, offset=consumer_amount
        )
        return message_to_record(message, offset=consumer_amount)

    def _fetch(
            self,
            partitions: Iterable[TopicPartition],
    ) -> Iterator[tuple[TopicPartition, ConsumerRecord[bytes, bytes]]]:

        if partitions:
            partitions_to_consume = list(partitions)
        else:
            partitions_to_consume = [
                TopicPartition(x, y)
                for x in self.subscribed_topic
                for y in self.kafka.partition_list(topic=x)
            ]

        random.shuffle(partitions_to_consume)

        for tp in partitions_to_consume:
            while True:
                record = self._fetch_one(tp.topic, tp.partition)
                if record is None:
                    # Partition has no available records; move to next
                    break

                yield tp, record

    async def getone(
            self, *partitions: TopicPartition
    ) -> Optional[ConsumerRecord[bytes, bytes]]:
        if self._is_closed:
            raise ConsumerStoppedError()

        for _, record in self._fetch(partitions):
            return record

        return None

    async def getmany(
            self,
            *partitions: TopicPartition,
            timeout_ms: int = 0,
            max_records: Optional[int] = None,
    ) -> dict[TopicPartition, list[ConsumerRecord[bytes, bytes]]]:
        if self._is_closed:
            raise ConsumerStoppedError()

        records = self._fetch(partitions)
        if max_records is not None:
            records = itertools.islice(records, max_records)

        result = collections.defaultdict(list)
        for tp, record in records:
            result[tp].append(record)

        return dict(result)
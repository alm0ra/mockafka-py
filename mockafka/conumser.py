from __future__ import annotations

import random
from copy import deepcopy

from mockafka.cluster_metadata import ClusterMetadata
from mockafka.kafka_store import KafkaStore
from mockafka.message import Message

__all__ = ["FakeConsumer"]


class FakeConsumer(object):
    """
    Mock implementation of the Confluent Kafka Consumer for testing purposes.

    Attributes:
    - kafka (KafkaStore): The in-memory storage for simulating Kafka behavior.
    - consumer_store (dict): Dictionary to store consumer offsets for each topic-partition.
    - subscribed_topic (list): List of topics subscribed by the consumer.

    Methods: - consume(num_messages=1, *args, **kwargs): Consume messages from subscribed topics. - close(*args,
    **kwargs): Close the consumer and reset state. - commit(message: Message = None, *args, **kwargs): Commit offsets
    for consumed messages. - list_topics(topic=None, *args, **kwargs): List topics (returns ClusterMetadata). - poll(
    timeout=None): Poll for messages from subscribed topics. - _get_key(topic, partition) -> str: Generate a unique
    key for a topic-partition pair. - subscribe(topics, on_assign=None, *args, **kwargs): Subscribe to one or more
    topics. - unsubscribe(*args, **kwargs): Unsubscribe from one or more topics. - assign(partitions): Assign
    partitions to the consumer (unsupported in mockafka). - unassign(*args, **kwargs): Unassign partitions (
    unsupported in mockafka). - assignment(*args, **kwargs) -> list: Get assigned partitions (unsupported in
    mockafka). - committed(partitions, timeout=None) -> list: Get committed offsets (unsupported in mockafka). -
    get_watermark_offsets(partition, timeout=None, *args, **kwargs) -> tuple: Get watermark offsets (unsupported in
    mockafka). - offsets_for_times(partitions, timeout=None) -> list: Get offsets for given times (unsupported in
    mockafka). - pause(partitions) -> None: Pause consumption from specified partitions (unsupported in mockafka). -
    position(partitions) -> list: Get the current position of the consumer in specified partitions (unsupported in
    mockafka). - resume(partitions) -> None: Resume consumption from specified partitions (unsupported in mockafka).
    - seek(partition) -> None: Seek to a specific offset in a partition (unsupported in mockafka). - store_offsets(
    message=None, *args, **kwargs) -> None: Store offsets for consumed messages (unsupported in mockafka). -
    consumer_group_metadata() -> None: Get consumer group metadata (unsupported in mockafka). - incremental_assign(
    partitions) -> None: Incrementally assign partitions (unsupported in mockafka). - incremental_unassign(
    partitions) -> None: Incrementally unassign partitions (unsupported in mockafka).
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the FakeConsumer.

        Parameters:
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).
        """
        self.kafka = KafkaStore()
        self.consumer_store = {}
        self.subscribed_topic: list = []

    def consume(self, num_messages=1, *args, **kwargs) -> list[Message]:
        """
        Consume messages from subscribed topics.

        Parameters:
        - num_messages (int): Number of messages to consume.
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).

        Returns:
        - Message or None: Consumed message or None if no message is available.
        """
        consumed_messages = []
        for count in range(num_messages):
            message = self.poll()
            if message:
                consumed_messages.append(message)

        return consumed_messages

    def close(self, *args, **kwargs):
        """
        Close the consumer and reset state.

        Parameters:
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).
        """
        self.consumer_store = {}
        self.subscribed_topic = []

    def commit(self, message: Message = None, *args, **kwargs):
        """
        Commit offsets for consumed messages.

        Parameters:
        - message (Message): Consumed message (unused).
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).
        """
        if message:
            topic = message.topic()
            partition = message.partition()
            key = self._get_key(topic=topic, partition=partition)
            if (
                self.kafka.get_partition_first_offset(topic, partition)
                <= self.consumer_store[key]
            ):
                self.kafka.set_first_offset(
                    topic=topic, partition=partition, value=self.consumer_store[key]
                )
            del self.consumer_store[key]

        else:
            for item in self.consumer_store:
                topic, partition = item.split("*")
                if (
                    self.kafka.get_partition_first_offset(topic, partition)
                    <= self.consumer_store[item]
                ):
                    self.kafka.set_first_offset(
                        topic=topic,
                        partition=partition,
                        value=self.consumer_store[item],
                    )

            self.consumer_store = {}

    def list_topics(self, topic=None, *args, **kwargs):
        """
        List topics (returns ClusterMetadata).

        Parameters:
        - topic: Topic name (unused).
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).

        Returns:
        - ClusterMetadata: Metadata of the listed topics.
        """
        return ClusterMetadata(topic=topic)

    def poll(self, timeout=None):
        """
        Poll for messages from subscribed topics.

        Parameters:
        - timeout (float): Poll timeout in seconds.

        Returns:
        - Message or None: Consumed message or None if no message is available.
        """
        if timeout:
            pass
            # sleep(timeout)
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

    def _get_key(self, topic, partition) -> str:
        """
        Generate a unique key for a topic-partition pair.

        Parameters:
        - topic: Topic name.
        - partition: Partition number.

        Returns:
        - str: Unique key for the topic-partition pair.
        """
        return f"{topic}*{partition}"

    def subscribe(self, topics, on_assign=None, *args, **kwargs):
        """
        Subscribe to one or more topics.

        Parameters:
        - topics (list): List of topics to subscribe to.
        - on_assign: Callback function for partition assignments (unused).
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).

        Raises:
        - KafkaException: If a subscribed topic does not exist in the Kafka store.
        """
        for topic in topics:
            if not self.kafka.is_topic_exist(topic):
                continue

            if topic not in self.subscribed_topic:
                self.subscribed_topic.append(topic)

    def unsubscribe(self, *args, **kwargs):
        """
        Unsubscribe from one or more topics.

        Parameters:
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments.

        Raises:
        - ValueError: If no 'topics' keyword argument is provided.
        """
        topics = kwargs.get("topics", [])
        for topic in topics:
            if topic in self.subscribed_topic:
                self.subscribed_topic.remove(topic)

    def assign(self, partitions):
        """
        Assign partitions to the consumer (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to assign (unused).
        """
        pass

    def unassign(self, *args, **kwargs):
        """
        Unassign partitions (unsupported in mockafka).

        Parameters:
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).
        """
        pass

    def assignment(self, *args, **kwargs) -> list:
        """
        Get assigned partitions (unsupported in mockafka).

        Returns:
        - list: An empty list.
        """
        return []

    def committed(self, partitions, timeout=None) -> list:
        """
        Get committed offsets (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to get committed offsets for (unused).
        - timeout: Timeout for the operation (unused).

        Returns:
        - list: An empty list.
        """
        return []

    def get_watermark_offsets(self, partition, timeout=None, *args, **kwargs) -> tuple:
        """
        Get watermark offsets (unsupported in mockafka).

        Parameters:
        - partition: Partition to get watermark offsets for (unused).
        - timeout: Timeout for the operation (unused).
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).

        Returns:
        - tuple: Tuple with watermark offsets (0, 0).
        """
        return (0, 0)

    def offsets_for_times(self, partitions, timeout=None) -> list:
        """
        Get offsets for given times (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to get offsets for (unused).
        - timeout: Timeout for the operation (unused).

        Returns:
        - list: An empty list.
        """
        return []

    def pause(self, partitions) -> None:
        """
        Pause consumption from specified partitions (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to pause consumption from (unused).

        Returns:
        - None
        """
        return None

    def position(self, partitions) -> list:
        """
        Get the current position of the consumer in specified partitions (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to get position for (unused).

        Returns:
        - list: An empty list.
        """
        return []

    def resume(self, partitions) -> None:
        """
        Resume consumption from specified partitions (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to resume consumption from (unused).

        Returns:
        - None
        """
        return None

    def seek(self, partition) -> None:
        """
        Seek to a specific offset in a partition (unsupported in mockafka).

        Parameters:
        - partition: Partition to seek in (unused).
        """
        pass

    def store_offsets(self, message=None, *args, **kwargs) -> None:
        """
        Store offsets for consumed messages (unsupported in mockafka).

        Parameters:
        - message: Consumed message (unused).
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).

        Returns:
        - None
        """
        return None

    def consumer_group_metadata(self) -> None:
        """
        Get consumer group metadata (unsupported in mockafka).

        Returns:
        - None
        """
        pass

    def incremental_assign(self, partitions) -> None:
        """
        Incrementally assign partitions (unsupported in mockafka).

        Parameters:
        - partitions: Partitions to incrementally assign (unused).

        Returns:
        - None
        """
        pass

    def incremental_unassign(self, partitions) -> None:
        pass

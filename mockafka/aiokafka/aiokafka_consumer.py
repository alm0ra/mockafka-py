from typing import Set

from mockafka.kafka_store import KafkaStore


class FakeAIOKafkaConsumer:
    def __init__(self, *args, **kwargs):
        """
        Initialize the FakeConsumer.

        Parameters:
        - args: Additional arguments (unused).
        - kwargs: Additional keyword arguments (unused).
        """
        self.kafka = KafkaStore()
        self.consumer_store = {}
        self.subscribed_topic: Set = set()

    async def start(self):
        self.consumer_store = {}
        self.subscribed_topic: Set = set()

    def assign(self):
        pass

    def assignment(self):
        pass

    async def stop(self):
        self.consumer_store = {}
        self.subscribed_topic: Set = set()

    async def commit(self):
        for item in self.consumer_store:
            topic, partition = item.split('*')
            if self.kafka.get_partition_first_offset(topic, partition) <= self.consumer_store[item]:
                self.kafka.set_first_offset(topic=topic, partition=partition, value=self.consumer_store[item])

        self.consumer_store = {}

    async def committed(self):
        pass

    async def topics(self):
        return self.subscribed_topic

    def partitions_for_topic(self, topic):
        pass

    async def position(self):
        pass

    def subscribe(self, topics: Set[str]):
        for topic in topics:
            if not self.kafka.is_topic_exist(topic):
                continue

            if topic not in self.subscribed_topic:
                self.subscribed_topic.append(topic)

    def subscribtion(self) -> Set[str]:
        return self.subscribed_topic

    def unsubscribe(self):
        self.subscribed_topic = []

    def _get_key(self, topic, partition) -> str:
        return f'{topic}*{partition}'

    async def getone(self):
        for topic in self.subscribed_topic:
            for partition in self.kafka.partition_list(topic=topic):
                first_offset = self.kafka.get_partition_first_offset(topic=topic, partition=partition)
                next_offset = self.kafka.get_partition_next_offset(topic=topic, partition=partition)
                consumer_amount = self.consumer_store.get(self._get_key(topic, partition))
                if first_offset == next_offset:
                    continue

                if consumer_amount == next_offset:
                    continue

                if consumer_amount is not None:
                    self.consumer_store[self._get_key(topic, partition)] += 1
                else:
                    self.consumer_store[self._get_key(topic, partition)] = first_offset + 1

                return self.kafka.get_message(topic=topic, partition=partition, offset=first_offset)

        return None

    async def getmany(self):
        # FIXME: must impelement
        return await self.getone()

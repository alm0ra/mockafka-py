from time import sleep

from mockafka import ClusterMetadata, Message
from mockafka.kafka_store import KafkaStore, KafkaException

__all__ = ["FakeConsumer"]


class FakeConsumer(object):
    def __init__(self, *args, **kwargs):
        self.kafka = KafkaStore()
        self.consumer_store = {}
        self.subscribed_topic: list = []

    def consume(self, num_messages=1, *args, **kwargs):
        return self.poll()

    def close(self, *args, **kwargs):
        self.consumer_store = {}

    def commit(self, message: Message = None, *args, **kwargs):
        if message:
            # we can keep (topic, partition, offset) in a message when we produce
            # and commit it by changing offset of topic i did not implement it yet
            pass

        else:
            for item in self.consumer_store:
                topic, partition = item.split('*')
                if self.kafka.get_partition_first_offset(topic, partition) <= self.consumer_store[item]:
                    self.kafka.set_first_offset(topic=topic, partition=partition, value=self.consumer_store[item] + 1)

            self.consumer_store = {}

    def list_topics(self, topic=None, *args, **kwargs):
        return ClusterMetadata(topic=topic)

    def poll(self, timeout=None):
        if timeout:
            sleep(timeout)

        for topic in self.subscribed_topic:
            for partition in self.kafka.partition_list(topic=topic):

                first_offset = self.kafka.get_partition_first_offset(topic=topic, partition=partition)
                next_offset = self.kafka.get_partition_next_offset(topic=topic, partition=partition)
                if first_offset == next_offset:
                    continue
                self.consumer_store[f'{topic}*{partition}'] = first_offset
                return self.kafka.get_message(topic=topic, partition=partition, offset=first_offset)

        return None

    def subscribe(self, topics, on_assign=None, *args, **kwargs):
        for topic in topics:
            if not self.kafka.is_topic_exist(topic):
                raise KafkaException(f'{topic} Does not exist in kafka.')

            if topic not in self.subscribed_topic:
                self.subscribed_topic.append(topic)

    def unsubscribe(self, *args, **kwargs):
        topics = kwargs['topics']
        for topic in topics:
            if topic in self.subscribed_topic:
                self.subscribed_topic.remove(topic)

    def assign(self, partitions):
        # This method Does not support in mockafka
        pass

    def unassign(self, *args, **kwargs):
        # This method Does not support in mockafka
        pass

    def assignment(self, *args, **kwargs):
        # This method Does not support in mockafka
        return []

    def committed(self, partitions, timeout=None):
        # This method Does not support in mockafka
        return []

    def get_watermark_offsets(self, partition, timeout=None, *args, **kwargs):
        # This method Does not support in mockafka
        return (0, 0)

    def offsets_for_times(self, partitions, timeout=None):
        # This method Does not support in mockafka
        return []

    def pause(self, partitions):
        # This method Does not support in mockafka
        return None

    def position(self, partitions):
        # This method Does not support in mockafka
        return []

    def resume(self, partitions):
        # This method Does not support in mockafka
        return None

    def seek(self, partition):
        # This method Does not support in mockafka
        pass

    def store_offsets(self, message=None, *args, **kwargs):
        # This method Does not support in mockafka
        return None

    def consumer_group_metadata(self):
        # This method Does not support in mockafka
        pass

    def incremental_assign(self, partitions):
        # This method Does not support in mockafka
        pass

    def incremental_unassign(self, partitions):
        # This method Does not support in mockafka
        pass

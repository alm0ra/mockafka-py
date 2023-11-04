"""
mock_topics = {
    'sample_topic':{
        1: [],
        2: [],
        3: [],
        4: []
    }
}

offset_store = {
    'sample_topic_1': {
        'first_offset': 0,
        'next_offset': 0,
    }
}
"""

mock_topics: dict[str, dict[int, list]] = {}

offset_store: dict[str, dict[str, int]] = {}


def _log(message: str):
    print(message)


def create_topic(topic: str, partition: int):
    if topic in mock_topics.keys():
        # Increase number of partitions
        len_of_current_partition = len(mock_topics[topic].keys())
        if partition > len_of_current_partition:
            _log(f"Increase Number of partition {topic} from {len_of_current_partition} to {partition}")
            for i in range(len_of_current_partition, partition):
                mock_topics[topic][i] = []
                offset_store[f'{topic}-{i}'] = {
                    'first_offset': 0,
                    'next_offset': 0
                }

        else:
            _log(f"{topic} Can not Decrease partition topic.")
    else:
        # create topic
        mock_topics[topic] = {}

        # create partitions
        for i in range(0, partition):
            mock_topics[topic][i] = []
            offset_store[f'{topic}-{i}'] = {
                'first_offset': 0,
                'next_offset': 0
            }


def produce(message: dict, topic: str, partition: int):
    if not mock_topics.get(topic):
        raise Exception(f'can not produce on {topic}, Topic Does Not Exist')

    if mock_topics[topic].get(partition, None) is None:
        raise Exception(f'can not produce on partition {partition} of {topic}, partition does not exist')

    # add message to topic
    mock_topics[topic][partition].append(message)

    # add offset
    offset_store[f'{topic}-{partition}']['next_offset'] += 1


class Consumer:
    def __init__(self):
        self.subscribed_topic = []
        self.consumer_store: dict[str, int] = {}

    def subscribe(self, topics: list):
        for topic in topics:
            if mock_topics.get(topic, None):
                if topic not in self.subscribed_topic:
                    self.subscribed_topic.append(topic)
            else:
                raise Exception(f'{topic} Does not exist in kafka.')

    def unsubscribe(self, topics: list):
        for topic in topics:
            self.subscribed_topic.delete(topic)

    def poll(self):
        for topic in mock_topics:
            for partition in mock_topics[topic]:
                topic_offset = offset_store[f'{topic}-{partition}']
                first_offset = topic_offset['first_offset']
                next_offset = topic_offset['next_offset']
                if first_offset == next_offset:
                    continue
                self.consumer_store[f'{topic}-{partition}'] = first_offset
                return mock_topics[topic][partition][first_offset]
        return None

    def commit(self, message: dict = None):
        if message:
            # we can keep (topic, partition, offset) in a message when we produce
            # and commit it by changing offset of topic i did not implement it yet
            pass

        else:
            for item in self.consumer_store:
                print(offset_store[item])
                print(self.consumer_store[item])
                if offset_store[item]['first_offset'] <= self.consumer_store[item]:
                    offset_store[item]['first_offset'] = self.consumer_store[item] + 1

            self.consumer_store = {}


create_topic("test", 6)
create_topic("test2", 6)

message1 = {
    "key": "key_test",
    "value": {"ali": 11}
}
message2 = {
    "key": "key_test3",
    "value": {"ali": 2}
}
message3 = {
    "key": "key_test3",
    "value": {"ali": 3}
}
message31 = {
    "key": "key_test31",
    "value": {"ali": 31}
}
message32 = {
    "key": "key_test31",
    "value": {"ali": 32}
}
message4 = {
    "key": "key_test4",
    "value": {"ali": 4}
}

produce(message1, "test", 1)
produce(message2, "test", 2)
produce(message2, "test2", 5)
produce(message3, "test", 3)
produce(message31, "test", 3)
produce(message31, "test2", 0)
produce(message32, "test", 3)

print("values in topic")
print(mock_topics)
print("offset")
print(offset_store)
consumer = Consumer()

consumer.subscribe(["test"])

message = consumer.poll()
print(message)

print("test commit")
consumer.commit()
print(offset_store)

print("test commit")

consumer.commit()
print(offset_store)


message = consumer.poll()
print(message)
message = consumer.poll()
print(message)
message = consumer.poll()
print(message)

consumer.commit()
message = consumer.poll()
print(message)

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

message = consumer.poll()
print(message)
consumer.commit()

mock_topics: dict[str, list] = {
    'topics': []
}


def create_topic(topic: str, partition: int):
    if topic in mock_topics['topics']:
        pass

    mock_topics['topics'].append(topic)
    for i in range(0, partition):
        if f'{topic}-{i}' not in mock_topics.keys():
            mock_topics[f'{topic}-{i}'] = []


def produce(event: dict, topic: str, partition: int):
    if topic not in mock_topics['topics']:
        raise Exception(f'can not produce on {topic}, Topic Does Not Exist')

    if f'{topic}-{partition}' not in mock_topics.keys():
        mock_topics[f'{topic}-{partition}'] = []

    mock_topics[f'{topic}-{partition}'].append(event)


class Consumer:
    def __init__(self):
        self.subscribed_topic = []
        self.message = None
        self.topic_partition = None

    def subscribe(self, topics: list):
        for topic in topics:
            if topic not in mock_topics['topics']:
                raise Exception(f'{topic} Does not exist')

            self.subscribed_topic.append(topic)

    def unsubscribe(self, topics: list):
        for topic in topics:
            if topic not in self.subscribed_topic:
                print(f"{topic} already unsubscribed")

            self.subscribed_topic.remove(topic)

    def poll(self, timeout=None):
        if self.message:
            return self.message

        for topic in self.subscribed_topic:
            for item in mock_topics.keys():
                if topic in item:
                    if not mock_topics[item]:
                        continue
                    self.message = mock_topics[item][0]
                    self.topic_partition = item
                    return self.message
            return None

    def commit(self):
        if self.message and self.topic_partition:
            mock_topics[self.topic_partition].remove(self.message)
            self.message = None
            self.topic_partition = None

    def poll1(self):
        pass

    def commit1(self, message=None, *args, **kwargs):
        pass



create_topic("ali", 16)
print(mock_topics)

produce({"key", "aliiiii"}, "ali", 1)
produce({"key", "2"}, "ali", 2)
produce({"key", "9"}, "ali", 9)
produce({"key", "3330"}, "ali", 3)
produce({"key", "3331"}, "ali", 3)
produce({"key", "444440"}, "ali", 4)
produce({"key", "444441"}, "ali", 4)

print(mock_topics)

consumer = Consumer()
consumer.subscribe(['ali'])

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

message = consumer.poll()
print(message)

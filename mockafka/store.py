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

NEW_OFFSET = {
    'first_offset': 0,
    'next_offset': 0
}


class KafkaStore:
    """
    In memory kafka store
    """

    @staticmethod
    def is_topic_exist(topic: str) -> bool:
        return topic in mock_topics.keys()

    @staticmethod
    def get_number_of_partition(topic: str) -> int:
        return len(mock_topics[topic].keys())

    @staticmethod
    def create_topic(topic: str):
        if mock_topics.get(topic, None) is None:
            raise Exception(f'{topic} exist is fake kaffa')

        mock_topics[topic] = {}

    @staticmethod
    def create_partition(topic: str, partitions: int):
        pass


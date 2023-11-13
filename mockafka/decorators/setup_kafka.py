from functools import wraps
from mockafka.admin_client import FakeAdminClientImpl, NewTopic


def setup_kafka(topics: [dict[str, str]]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract parameters from the decorator_args
            fake_admin = FakeAdminClientImpl()

            for item in topics:
                topic = item.get('topic', None)
                partition = item.get('partition', None)
                fake_admin.create_topics(topics=[NewTopic(topic=topic, num_partitions=partition)])

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


from functools import wraps
from mockafka import FakeProducer


def bulk_produce(list_of_messages: list[dict[str, str]]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fake_producer = FakeProducer()
            # Extract parameters from the decorator_args
            for item in list_of_messages:
                value = item.get('value', None)
                key = item.get('key', None)
                topic = item.get('topic', None)
                partition = item.get('partition', None)
                timestamp = item.get('timestamp', None)
                headers = item.get('headers', None)

                fake_producer.produce(topic=topic, partition=partition, value=value, key=key,
                                      timestamp=timestamp, headers=headers)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

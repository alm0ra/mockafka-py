from functools import wraps
from mockafka import FakeProducer


def produce(**decorator_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract parameters from the decorator_args
            topic = decorator_args.get('topic', None)
            value = decorator_args.get('value', None)
            key = decorator_args.get('key', None)
            headers = decorator_args.get('headers', None)
            partition = decorator_args.get('partition', None)

            fake_producer = FakeProducer()

            fake_producer.produce(topic=topic, partition=partition, value=value, key=key, headers=headers)
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


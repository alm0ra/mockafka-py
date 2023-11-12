from functools import wraps
from mockafka import FakeConsumer


def consume(topics: list[str], auto_commit: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract parameters from the decorator_args

            fake_consumer = FakeConsumer()
            fake_consumer.subscribe(topics=topics)

            # not complete yet
            # while True:
            #     message = fake_consumer.poll()

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


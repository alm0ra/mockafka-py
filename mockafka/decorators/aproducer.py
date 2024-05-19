from __future__ import annotations

from functools import wraps

from mockafka.aiokafka import FakeAIOKafkaProducer


def aproduce(**decorator_args):
    """
    aproduce is a decorator for simulating message production using a FakeAIOKafkaProducer.

    It extracts the following parameters from the decorator args:

    - topic (str): Topic to produce to
    - value (str): Message value
    - key (str): Message key
    - headers (dict): Message headers
    - partition (int): Topic partition to produce to

    The decorator creates a FakeAIOKafkaProducer instance and calls send()
    to produce a message with the provided parameters.

    It then calls the decorated function.

    This allows you to test message production logic using the fake producer.

    Example usage:

    @aproduce(topic='test', value='foo')
    async def produce_message():
      # test logic here

    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract parameters from the decorator_args
            topic = decorator_args.get("topic", None)
            value = decorator_args.get("value", None)
            key = decorator_args.get("key", None)
            headers = decorator_args.get("headers", None)
            partition = decorator_args.get("partition", None)

            # Create a FakeProducer instance and produce the message
            fake_producer = FakeAIOKafkaProducer()
            await fake_producer.send(
                topic=topic, partition=partition, value=value, key=key, headers=headers
            )

            # Call the original function
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator

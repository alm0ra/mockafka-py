from __future__ import annotations

from functools import wraps

from mockafka.aiokafka import FakeAIOKafkaConsumer


def aconsume(topics: list[str], auto_commit: bool = True):
    """
    aconsume is a decorator for simulating async message consumption using a FakeAIOKafkaConsumer.

    Parameters:
    - topics (list[str]): List of topic names to subscribe to.
    - auto_commit (bool): Whether to automatically commit offsets after consuming messages. Default True.

    The decorator subscribes a FakeAIOKafkaConsumer to the specified topics and consumes messages in a loop.

    For each message, it calls the decorated function, passing the message as a keyword argument.

    After consuming all available messages, it calls the decorated function again without the message arg.

    This allows you to test message consumption and processing logic using the fake consumer.

    Example usage:

    @aconsume(topics=['test'], auto_commit=False)
    async def process_message(message):
      # message processing logic

    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a FakeConsumer instance and subscribe to specified topics
            fake_consumer = FakeAIOKafkaConsumer()
            fake_consumer.subscribe(topics=topics)

            # Simulate message consumption
            while True:
                message = await fake_consumer.getone()

                # Break if no more messages
                if message is None:
                    break

                # Call the original function with the consumed message
                await func(message=message, *args, **kwargs)

            # Call the original function without a message parameter
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator

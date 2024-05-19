from __future__ import annotations

from functools import wraps
from mockafka import FakeConsumer


def consume(topics: list[str], auto_commit: bool = True):
    """
    A decorator for simulating message consumption using a FakeConsumer.

    Parameters:
    - topics (list[str]): A list of topics to subscribe to.
    - auto_commit (bool): Whether to automatically commit offsets after consuming messages.

    Example Usage:
    ```python
    @consume(topics=['test_topic'], auto_commit=False)
    def test_function(message):
        # Your test logic for processing the consumed message here
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a FakeConsumer instance and subscribe to specified topics
            fake_consumer = FakeConsumer()
            fake_consumer.subscribe(topics=topics)

            # Simulate message consumption
            while True:
                message = fake_consumer.poll()

                # Break if no more messages
                if message is None:
                    break

                # Call the original function with the consumed message
                func(message=message, *args, **kwargs)

            # Call the original function without a message parameter
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

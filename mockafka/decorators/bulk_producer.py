from __future__ import annotations

from functools import wraps
from mockafka import FakeProducer


def bulk_produce(list_of_messages: list[dict[str, str]]):
    """
    A decorator for bulk-producing messages using a FakeProducer.

    Parameters:
    - list_of_messages (list[dict[str, str]]): A list of dictionaries containing message details.

    Each dictionary should have the following optional keys:
    - 'value': The value of the message.
    - 'key': The key of the message.
    - 'topic': The topic to produce the message.
    - 'partition': The partition of the topic.
    - 'timestamp': The timestamp of the message.
    - 'headers': The headers of the message.

    Example Usage:
    ```python
    @bulk_produce(list_of_messages=[{'topic': 'test_topic', 'value': 'test_value1'}, {...}])
    def test_function():
        # Your test logic here
    ```

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a FakeProducer instance for producing messages
            fake_producer = FakeProducer()

            # Extract parameters from each message dictionary and produce messages
            for item in list_of_messages:
                value = item.get("value", None)
                key = item.get("key", None)
                topic = item.get("topic", None)
                partition = item.get("partition", None)
                timestamp = item.get("timestamp", None)
                headers = item.get("headers", None)

                # Produce the message using the FakeProducer
                fake_producer.produce(
                    topic=topic,
                    partition=partition,
                    value=value,
                    key=key,
                    timestamp=timestamp,
                    headers=headers,
                )

            # Call the original function
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

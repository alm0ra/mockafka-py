from functools import wraps
from mockafka.aiokafka import FakeAIOKafkaProducer


def aproduce(**decorator_args):
    """
    A decorator for simulating message production using a FakeProducer.

    Parameters:
    - topic (str): The topic to produce the message.
    - value (str): The value of the message.
    - key (str): The key of the message.
    - headers (str): The headers of the message.
    - partition (str): The partition of the topic.

    Example Usage:
    ```python
    @produce(topic='test_topic', value='test_value', key='test_key', headers=None, partition=0)
    def test_function():
        # Your test logic here
    ```
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract parameters from the decorator_args
            topic = decorator_args.get('topic', None)
            value = decorator_args.get('value', None)
            key = decorator_args.get('key', None)
            headers = decorator_args.get('headers', None)
            partition = decorator_args.get('partition', None)

            # Create a FakeProducer instance and produce the message
            fake_producer = FakeAIOKafkaProducer()
            await fake_producer.send(
                topic=topic,
                partition=partition,
                value=value,
                key=key,
                headers=headers
            )

            # Call the original function
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator

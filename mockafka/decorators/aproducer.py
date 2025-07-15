from __future__ import annotations

from functools import wraps
from typing import Awaitable, Callable, Optional, TypeVar

from typing_extensions import ParamSpec

from mockafka.aiokafka import FakeAIOKafkaProducer

P = ParamSpec('P')
R = TypeVar('R')


def aproduce(
    *,
    topic: str,
    value: Optional[bytes] = None,
    key: Optional[bytes] = None,
    partition: int = 0,
    headers: Optional[list[tuple[str, Optional[bytes]]]] = None,
) -> Callable[
    [Callable[P, Awaitable[R]]],
    Callable[P, Awaitable[R]],
]:
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

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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

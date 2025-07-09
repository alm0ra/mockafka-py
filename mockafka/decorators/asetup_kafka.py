from __future__ import annotations

from functools import wraps
from typing import Awaitable, Callable, TypeVar

from aiokafka.admin import NewTopic  # type: ignore[import-untyped]
from typing_extensions import ParamSpec

from mockafka.aiokafka import FakeAIOKafkaAdmin
from mockafka.decorators.typing import TopicConfig

P = ParamSpec('P')
R = TypeVar('R')


def asetup_kafka(
    topics: list[TopicConfig],
    clean: bool = False,
) -> Callable[
    [Callable[P, Awaitable[R]]],
    Callable[P, Awaitable[R]],
]:
    """
    asetup_kafka is a decorator for setting up mock Kafka topics using a FakeAIOKafkaAdminClient.

    It takes the following parameters:

    - topics (list[dict]): List of topic configs, each containing:
        - topic (str): Topic name
        - partition (int): Partition count
    - clean (bool): Whether to clean existing topics first. Default False.

    The decorator creates a FakeAIOKafkaAdminClient instance and uses it to create
    the specified topics.

    This allows you to setup mock Kafka topics and partitions at test setup.

    Example usage:

    @asetup_kafka(topics=[{'topic': 'test', 'partitions': 1}])
    async def test_function():
      # test logic

    """

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Create a FakeAdminClient instance with the specified clean option
            fake_admin = FakeAIOKafkaAdmin(clean=clean)

            # Create specified topics using the FakeAdminClient
            for item in topics:
                topic = item.get("topic", None)
                partition = item.get("partition", None)
                await fake_admin.create_topics(
                    new_topics=[
                        NewTopic(
                            name=topic, num_partitions=partition, replication_factor=1
                        )
                    ]
                )

            # Call the original function
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator

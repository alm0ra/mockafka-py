from __future__ import annotations

from functools import wraps

from aiokafka.admin import NewTopic

from mockafka.aiokafka import FakeAIOKafkaAdmin


def asetup_kafka(topics: [dict[str, str]], clean: bool = False):
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

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
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

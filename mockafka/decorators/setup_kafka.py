from __future__ import annotations

from functools import wraps
from mockafka.admin_client import FakeAdminClientImpl, NewTopic


def setup_kafka(topics: [dict[str, str]], clean: bool = False):
    """
    A decorator for setting up Mockafka with specified topics using a FakeAdminClient.

    Parameters:
    - topics (list[dict[str, str]]): A list of dictionaries containing topic details.
        Each dictionary should have the keys 'topic' and 'partition'.
    - clean (bool): Option to have a clean Kafka (remove existing topics) or not.

    Example Usage:
    ```python
    @setup_kafka(topics=[{'topic': 'test_topic', 'partition': 5}], clean=True)
    def test_function():
        # Your test logic here
    ```
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a FakeAdminClient instance with the specified clean option
            fake_admin = FakeAdminClientImpl(clean=clean)

            # Create specified topics using the FakeAdminClient
            for item in topics:
                topic = item.get("topic", None)
                partition = item.get("partition", None)
                fake_admin.create_topics(
                    topics=[NewTopic(topic=topic, num_partitions=partition)]
                )

            # Call the original function
            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

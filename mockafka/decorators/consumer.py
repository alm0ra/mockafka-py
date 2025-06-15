from __future__ import annotations

import inspect
from functools import wraps

from mockafka.consumer import FakeConsumer


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
        # Get the function signature
        sig = inspect.signature(func)

        # Create a new signature with default values for message parameters
        new_params = []
        for param_name, param in sig.parameters.items():
            if param_name == 'message' and param.default == inspect.Parameter.empty:
                # Add default value to prevent pytest from treating it as a fixture
                new_param = param.replace(default=None)
                new_params.append(new_param)
            else:
                new_params.append(param)

        new_sig = sig.replace(parameters=new_params)

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
                func(message=message, *args, **kwargs)  # noqa: B026  # TODO: fix unpacking

            # Call the original function without a message parameter
            result = func(message=None, *args, **kwargs)  # noqa: B026  # TODO: fix unpacking
            return result

        # Apply the new signature to the wrapper
        wrapper.__signature__ = new_sig
        return wrapper

    return decorator

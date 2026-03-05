from __future__ import annotations


class MockafkaNoMessagesError(Exception):
    """Raised by FakeAIOKafkaConsumer.getone() when no messages are available.

    The real aiokafka consumer would block indefinitely in this situation,
    but since mockafka is a testing mock, blocking would cause tests to hang.
    This exception is raised instead to provide a clear signal.

    To handle this in your tests, either:
      - Ensure messages are produced before consuming
      - Catch this exception explicitly
    """

    def __init__(self, message: str | None = None) -> None:
        super().__init__(
            message
            or (
                "No messages available. The real aiokafka consumer would block "
                "indefinitely here, but mockafka raises this error instead to "
                "prevent tests from hanging."
            )
        )

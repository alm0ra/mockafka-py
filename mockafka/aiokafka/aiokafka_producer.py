from __future__ import annotations

from mockafka.kafka_store import KafkaStore
from mockafka.message import Message


class FakeAIOKafkaProducer:
    """
    FakeAIOKafkaProducer is a mock implementation of aiokafka's AIOKafkaProducer.

    It allows mocking a kafka producer for testing purposes.

    Parameters:
    - args, kwargs: Passed to superclass init, not used here.

    Attributes:
    - kafka: KafkaStore instance for underlying storage.

    Methods:
    - _produce(): Create a Message and produce to KafkaStore.
      Takes topic, value, and optional partition.
    - start(): No-op.
    - stop(): No-op.
    - send(): Call _produce() with kwargs.
    - send_and_wait(): Call send().
    """

    def __init__(self, *args, **kwargs) -> None:
        self.kafka = KafkaStore()

    async def _produce(self, topic, value=None, *args, **kwargs) -> None:
        # create a message and call produce kafka
        message = Message(value=value, topic=topic, *args, **kwargs)
        self.kafka.produce(message=message, topic=topic, partition=kwargs["partition"])

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def send(
        self,
        topic,
        value=None,
        key=None,
        partition=0,
        timestamp_ms=None,
        headers=None,
    ) -> None:
        await self._produce(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            headers=headers,
            timestamp_ms=timestamp_ms,
        )

    async def send_and_wait(
        self,
        topic,
        value=None,
        key=None,
        partition=0,
        timestamp_ms=None,
        headers=None,
    ) -> None:
        await self._produce(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            headers=headers,
            timestamp_ms=timestamp_ms,
        )

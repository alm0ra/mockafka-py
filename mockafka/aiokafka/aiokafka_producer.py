from asyncio import create_task

from mockafka.kafka_store import KafkaStore
from mockafka.message import Message


class FakeAIOKafkaProducer:
    def __init__(self, *args, **kwargs):
        self.kafka = KafkaStore()

    async def _produce(self, topic, value=None, *args, **kwargs):
        # create a message and call produce kafka
        message = Message(value=value, topic=topic, *args, **kwargs)
        self.kafka.produce(message=message, topic=topic, partition=kwargs['partition'])

    async def start(self):
        pass

    async def send(self, *args, **kwargs):
        await self._produce(**kwargs)

    async def send_and_wait(self, *args, **kwargs):
        await self.send()

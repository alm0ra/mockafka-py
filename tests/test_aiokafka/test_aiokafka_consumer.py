from __future__ import annotations

import itertools
from unittest import IsolatedAsyncioTestCase

import pytest
from aiokafka.errors import ConsumerStoppedError  # type: ignore[import-untyped]
from aiokafka.structs import (  # type: ignore[import-untyped]
    ConsumerRecord,
    TopicPartition,
)

from mockafka.aiokafka import (
    FakeAIOKafkaAdmin,
    FakeAIOKafkaConsumer,
    FakeAIOKafkaProducer,
)
from mockafka.kafka_store import KafkaStore


@pytest.mark.asyncio
class TestAIOKAFKAFakeConsumer(IsolatedAsyncioTestCase):
    def summarise(
        self,
        records: list[ConsumerRecord],
    ) -> list[tuple[str | None, str | None]]:
        return [(x.key, x.value) for x in records]

    def setUp(self) -> None:
        self.kafka = KafkaStore(clean=True)
        self.producer = FakeAIOKafkaProducer()
        self.consumer = FakeAIOKafkaConsumer()
        self.admin = FakeAIOKafkaAdmin()
        self.test_topic = "test_topic"

    @pytest.fixture(autouse=True)
    def topic(self):
        self.test_topic = "test_topic"

    def create_topic(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=16)

    async def produce_message(self):
        await self.producer.send(
            topic=self.test_topic, partition=0, key="test", value="test"
        )
        await self.producer.send(
            topic=self.test_topic, partition=0, key="test1", value="test1"
        )

    async def test_consume(self):
        await self.test_poll_with_commit()

    async def test_start(self):
        # check consumer store is empty
        await self.consumer.start()
        self.assertEqual(self.consumer.consumer_store, {})

        # change consumer store and check it's changed
        self.consumer.consumer_store = {"key", "value"}
        self.assertNotEqual(self.consumer.consumer_store, {})

        # close consumer and check consumer store and consume return none
        await self.consumer.stop()
        self.assertEqual(self.consumer.consumer_store, {})

        await self.consumer.start()
        self.assertIsNone(await self.consumer.getone())

    async def test_poll_without_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        message = await self.consumer.getone()
        self.assertEqual(message.value, b"test")
        message = await self.consumer.getone()
        self.assertEqual(message.value, b"test1")

        self.assertIsNone(await self.consumer.getone())
        self.assertIsNone(await self.consumer.getone())

    async def test_partition_specific_poll_without_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        message = await self.consumer.getone(
            TopicPartition(self.test_topic, 2),
        )
        self.assertIsNone(message)

        message = await self.consumer.getone(
            TopicPartition(self.test_topic, 0),
        )
        self.assertEqual(message.value, b"test")

    async def test_poll_with_commit(self):
        self.create_topic()
        await self.produce_message()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        message = await self.consumer.getone()
        await self.consumer.commit()
        self.assertEqual(message.value, b"test")

        message = await self.consumer.getone()
        await self.consumer.commit()
        self.assertEqual(message.value, b"test1")

        self.assertIsNone(await self.consumer.getone())
        self.assertIsNone(await self.consumer.getone())

    async def test_getmany_without_commit(self):
        self.create_topic()
        await self.produce_message()
        await self.producer.send(
            topic=self.test_topic, partition=2, key="test2", value="test2"
        )
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        # Order unknown as partition order is not predictable
        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany()).items()
        }
        self.assertEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
                TopicPartition(self.test_topic, partition=2): [
                    (b"test2", b"test2"),
                ],
            },
            messages,
        )

        self.assertEqual({}, await self.consumer.getmany())

    async def test_getmany_with_limit_without_commit(self):
        self.create_topic()
        await self.produce_message()
        await self.producer.send(
            topic=self.test_topic, partition=0, key="test2", value="test2"
        )
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()
        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany(max_records=2)).items()
        }
        self.assertEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
            },
            messages,
        )

        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany()).items()
        }
        self.assertEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test2", b"test2"),
                ],
            },
            messages,
        )

        self.assertEqual({}, await self.consumer.getmany())

    async def test_getmany_specific_poll_without_commit(self):
        self.create_topic()
        await self.produce_message()
        await self.producer.send(
            topic=self.test_topic, partition=1, key="test2", value="test2"
        )
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        target = TopicPartition(self.test_topic, 0)

        # Order unknown as partition order is not predictable
        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany(target)).items()
        }
        self.assertCountEqual(
            {
                target: [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
            },
            messages,
        )

        self.assertEqual({}, await self.consumer.getmany(target))

    async def test_getmany_with_commit(self):
        self.create_topic()
        await self.produce_message()
        await self.producer.send(
            topic=self.test_topic, partition=2, key="test2", value="test2"
        )
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        # Order unknown, though we can check the counts eagerly
        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany(max_records=2)).items()
        }
        self.assertEqual(
            2,
            len(tuple(itertools.chain.from_iterable(messages.values()))),
        )
        await self.consumer.commit()

        for tp, msgs in (await self.consumer.getmany()).items():
            messages.setdefault(tp, []).extend(self.summarise(msgs))

        self.assertCountEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
                TopicPartition(self.test_topic, partition=2): [
                    (b"test2", b"test2"),
                ],
            },
            messages,
        )

        self.assertEqual({}, await self.consumer.getmany())

    async def test_subscribe(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)

    async def test_subscribe_pattern(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)
        self.kafka.create_partition(topic="other_topic", partitions=10)

        self.consumer.subscribe(pattern=r"^test_.*")

        topics = [self.test_topic, test_topic_2]
        self.assertEqual(self.consumer.subscribed_topic, topics)

    async def test_subscribe_topic_not_exist(self):
        self.create_topic()
        topics = [self.test_topic, "missing-topic"]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, [self.test_topic])

    async def test_lifecycle(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)

        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)

        await self.consumer.start()

        self.assertEqual(self.consumer.subscribed_topic, topics)

        await self.produce_message()

        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany()).items()
        }
        self.assertEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
            },
            messages,
        )

        await self.consumer.stop()

        self.assertEqual(self.consumer.subscribed_topic, topics)

        await self.consumer.start()
        # TODO: work out what the expected behaviour is here -- should we start
        # from a zero offset, or should that also persist?
        messages = {
            tp: self.summarise(msgs)
            for tp, msgs in (await self.consumer.getmany()).items()
        }
        self.assertEqual(
            {
                TopicPartition(self.test_topic, partition=0): [
                    (b"test", b"test"),
                    (b"test1", b"test1"),
                ],
            },
            messages,
        )

    async def test_unsubscribe(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]

        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)
        self.consumer.unsubscribe()
        self.assertEqual(self.consumer.subscribed_topic, [])

    async def test_consumer_is_stopped(self):
        self.kafka.create_partition(topic=self.test_topic, partitions=10)

        topics = [self.test_topic]

        self.consumer.subscribe(topics=topics)
        with self.assertRaises(ConsumerStoppedError):
            await self.consumer.getone()

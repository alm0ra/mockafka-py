from __future__ import annotations

import sys
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

if sys.version_info < (3, 10):
    def aiter(async_iterable):  # noqa: A001
        return async_iterable.__aiter__()

    async def anext(async_iterable):  # noqa: A001
        return await async_iterable.__anext__()


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

    async def produce_two_messages(self):
        await self.producer.send(
            topic=self.test_topic, partition=0, key=b"test", value=b"test"
        )
        await self.producer.send(
            topic=self.test_topic, partition=0, key=b"test1", value=b"test1"
        )

    async def test_async_iterator(self):
        self.create_topic()
        await self.produce_two_messages()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        iterator = aiter(self.consumer)
        message = await anext(iterator)
        self.assertEqual(message.value, b"test")

        message = await anext(iterator)
        self.assertEqual(message.value, b"test1")

        # Technically at this point aiokafka's consumer would block
        # indefinitely, however since that's not useful in tests we instead stop
        # iterating.
        with pytest.raises(StopAsyncIteration):
            await anext(iterator)

    async def test_async_iterator_closed_early(self):
        self.create_topic()
        await self.produce_two_messages()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        iterator = aiter(self.consumer)
        message = await anext(iterator)
        self.assertEqual(message.value, b"test")

        await self.consumer.stop()

        with pytest.raises(StopAsyncIteration):
            await anext(iterator)

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
        await self.produce_two_messages()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        message = await self.consumer.getone()
        self.assertEqual(message.value, b"test")
        message = await self.consumer.getone()
        self.assertEqual(message.value, b"test1")

        self.assertIsNone(await self.consumer.getone())
        self.assertIsNone(await self.consumer.getone())

        await self.consumer.stop()

        # We didn't commit, so we should see the same messages again
        async with FakeAIOKafkaConsumer(self.test_topic) as new_consumer:
            message = await new_consumer.getone()
            self.assertEqual(message.value, b"test")
            message = await new_consumer.getone()
            self.assertEqual(message.value, b"test1")

    async def test_partition_specific_poll_without_commit(self):
        self.create_topic()
        await self.produce_two_messages()
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

        await self.consumer.stop()

        # We didn't commit, so we should see the same results again
        async with FakeAIOKafkaConsumer(self.test_topic) as new_consumer:
            message = await new_consumer.getone(TopicPartition(self.test_topic, 0))
            self.assertEqual(message.value, b"test")

            message = await new_consumer.getone(TopicPartition(self.test_topic, 2))
            self.assertIsNone(message)

    async def test_poll_with_commit(self):
        self.create_topic()
        await self.produce_two_messages()
        self.consumer.subscribe(topics=[self.test_topic])
        await self.consumer.start()

        message = await self.consumer.getone()
        await self.consumer.commit()
        self.assertEqual(message.value, b"test")

        # We committed, so a new consumer should see the next message in the topic
        async with FakeAIOKafkaConsumer(self.test_topic) as new_consumer:
            message = await new_consumer.getone()
            self.assertEqual(message.value, b"test1")
            await new_consumer.commit()

        # Back to the original consumer should see empty now that both messages
        # are consumed
        self.assertIsNone(await self.consumer.getone())

    async def test_partition_specific_poll_with_commit(self):
        topic_a = "topic-a"
        topic_b = "topic-b"

        self.kafka.create_partition(topic=topic_a, partitions=2)
        self.kafka.create_partition(topic=topic_b, partitions=2)

        await self.producer.send(
            topic=topic_a, partition=0, key=b"a0.0", value=b"a0.0"
        )
        await self.producer.send(
            topic=topic_a, partition=0, key=b"a0.1", value=b"a0.1"
        )
        await self.producer.send(
            topic=topic_a, partition=1, key=b"a1.0", value=b"a1.0"
        )
        await self.producer.send(
            topic=topic_b, partition=0, key=b"b0.0", value=b"b0.0"
        )
        await self.producer.send(
            topic=topic_b, partition=0, key=b"b0.1", value=b"b0.1"
        )

        self.consumer.subscribe(topics=[topic_a, topic_b])
        await self.consumer.start()

        await self.consumer.getmany(
            TopicPartition(topic_a, 0),
            TopicPartition(topic_a, 1),
        )
        await self.consumer.getone(
            TopicPartition(topic_b, 0),
        )

        # Only commit the first messages from each partition on topic a -- this
        # leaves one message non-committed on the 0th partition and shouldn't
        # affect either our logical or committed position on topic b.
        await self.consumer.commit({
            TopicPartition(topic_a, 0): 1,
            TopicPartition(topic_a, 1): 1,
        })

        result = await self.consumer.getmany()
        simple_result = {
            tp: [x.value for x in msgs]
            for tp, msgs in result.items()
        }

        assert simple_result == {
            # Topic A is fully consumed, even though not fully committed, so no
            # further results here.

            # One more message on topic B partition 0
            TopicPartition(topic_b, 0): [b"b0.1"],
        }, "Wrong result after commit"

        # We didn't commit, so we should see the same results again
        async with FakeAIOKafkaConsumer(topic_a, topic_b) as new_consumer:
            new_result = await new_consumer.getmany()
            simple_new_result = {
                tp: [x.value for x in msgs]
                for tp, msgs in new_result.items()
            }

            assert simple_new_result == {
                # Topic A partition 1 wasn't fully committed -- the remaining
                # message should be here.
                TopicPartition(topic_a, 0): [b"a0.1"],
                # Topic B wasn't committed -- all messages appear
                TopicPartition(topic_b, 0): [b"b0.0", b"b0.1"],
            }, "Wrong result from fresh consumer"

    async def test_getmany_without_commit(self):
        self.create_topic()
        await self.produce_two_messages()
        await self.producer.send(
            topic=self.test_topic, partition=2, key=b"test2", value=b"test2"
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
        await self.produce_two_messages()
        await self.producer.send(
            topic=self.test_topic, partition=0, key=b"test2", value=b"test2"
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
        await self.produce_two_messages()
        await self.producer.send(
            topic=self.test_topic, partition=1, key=b"test2", value=b"test2"
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
        await self.produce_two_messages()
        await self.producer.send(
            topic=self.test_topic, partition=2, key=b"test2", value=b"test2"
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

        await self.produce_two_messages()

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

    async def test_context_manager(self):
        test_topic_2 = "test_topic_2"
        self.kafka.create_partition(topic=self.test_topic, partitions=10)
        self.kafka.create_partition(topic=test_topic_2, partitions=10)

        topics = [self.test_topic, test_topic_2]
        self.consumer.subscribe(topics=topics)

        self.assertEqual(self.consumer.subscribed_topic, topics)

        async with self.consumer as consumer:
            self.assertEqual(self.consumer, consumer)
            await self.produce_two_messages()

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

        self.assertEqual(self.consumer.subscribed_topic, topics)

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

        with self.assertRaises(ConsumerStoppedError):
            aiter(self.consumer)

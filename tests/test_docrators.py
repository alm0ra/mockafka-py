from __future__ import annotations

from unittest import TestCase

from mockafka import FakeConsumer, Message, bulk_produce, produce, setup_kafka
from mockafka.admin_client import FakeAdminClientImpl, NewTopic
from mockafka.decorators.consumer import consume
from mockafka.decorators.typing import MessageDict
from mockafka.producer import FakeProducer

sample_for_bulk_produce: list[MessageDict] = [
    {
        "key": "test_key",
        "value": "test_value",
        "topic": "test",
        "partition": 0,
    },
    {
        "key": "test_key1",
        "value": "test_value1",
        "topic": "test",
        "partition": 1,
    },
]


class TestDecorators(TestCase):
    def setUp(self) -> None:
        self.admin = FakeAdminClientImpl(clean=True)
        self.admin.create_topics([NewTopic(topic="test", num_partitions=16)])
        self.consumer = FakeConsumer()
        self.producer = FakeProducer()
        self.fake_producer = FakeProducer()

    @produce(topic="test", key="test_key", value="test_value", partition=4)
    def test_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])
        message = self.consumer.poll()

        self.assertEqual(message.value(payload=None), b"test_value")
        self.assertEqual(message.key(), b"test_key")

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @produce(topic="test", key="test_key", value="test_value", partition=4)
    @produce(topic="test", key="test_key1", value="test_value1", partition=0)
    def test_produce_twice(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])

        # Order unknown as partition order is not predictable
        messages = [
            (x.key(), x.value(payload=None))
            for x in (
                self.consumer.poll(),
                self.consumer.poll(),
            )
        ]
        self.assertCountEqual(
            [
                (b"test_key", b"test_value"),
                (b"test_key1", b"test_value1"),
            ],
            messages,
        )

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @bulk_produce(list_of_messages=sample_for_bulk_produce)
    def test_bulk_produce_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test"])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), b"test_value")
        self.assertEqual(message.key(), b"test_key")

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), b"test_value1")
        self.assertEqual(message.key(), b"test_key1")

        # commit message and check
        self.consumer.commit()

        # check there is no message in mock kafka
        self.assertIsNone(self.consumer.poll())

    @setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    def test_produce_with_kafka_setup_decorator(self):
        # subscribe to topic and get message
        self.consumer.subscribe(topics=["test_topic"])

        message = self.consumer.poll()
        self.assertEqual(message.value(payload=None), b"test_value1")
        self.assertEqual(message.key(), b"test_")

    @setup_kafka(topics=[{"topic": "test_topic", "partition": 16}])
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @produce(topic="test_topic", partition=5, key="test_", value="test_value1")
    @consume(topics=["test_topic"])
    def test_consumer_decorator(self, message: Message | None = None):
        if message is None:
            return

        self.assertEqual(message.key(), b"test_")
        self.assertEqual(message._partition, 5)

    # NEW TEST CASES FOR PYTEST FIXTURE ISSUE FIX

    @setup_kafka(topics=[{"topic": "pytest_fix_test", "partition": 16}])
    @produce(topic="pytest_fix_test", key="fix_key", value="fix_value", partition=3)
    @consume(topics=["pytest_fix_test"])
    def test_consume_decorator_without_default_parameter(self, message):
        """
        Test case for the original pytest fixture issue.
        This test verifies that @consume decorator works with function parameters
        that don't have default values, which used to cause pytest to treat 'message'
        as a fixture and fail with 'fixture message not found'.

        This reproduces the exact issue from the bug report.
        """
        if message is None:
            return

        # Verify the message was consumed correctly
        self.assertEqual(message.key(), "fix_key")
        self.assertEqual(message.value(payload=None), "fix_value")
        self.assertEqual(message.partition(), 3)

    @setup_kafka(topics=[{"topic": "pytest_fix_test2", "partition": 16}])
    @produce(topic="pytest_fix_test2", key="fix_key2", value="fix_value2", partition=7)
    @consume(topics=["pytest_fix_test2"])
    def test_consume_decorator_with_explicit_default(self, message=None):
        """
        Test case to ensure backward compatibility.
        This verifies that functions with explicit default values still work correctly
        after the pytest fixture fix.
        """
        if message is None:
            return

        # Verify the message was consumed correctly
        self.assertEqual(message.key(), "fix_key2")
        self.assertEqual(message.value(payload=None), "fix_value2")
        self.assertEqual(message.partition(), 7)

    @setup_kafka(topics=[{"topic": "multiple_messages_test", "partition": 16}])
    @produce(topic="multiple_messages_test", key="msg1_key", value="msg1_value", partition=1)
    @produce(topic="multiple_messages_test", key="msg2_key", value="msg2_value", partition=2)
    @produce(topic="multiple_messages_test", key="msg3_key", value="msg3_value", partition=3)
    @consume(topics=["multiple_messages_test"])
    def test_consume_decorator_multiple_messages_no_default(self, message):
        """
        Test case for multiple message consumption without default parameter.
        This ensures the fix works correctly when multiple messages are produced
        and consumed, and the function parameter has no default value.
        """
        if message is None:
            return

        # Verify we receive one of the expected messages
        expected_keys = ["msg1_key", "msg2_key", "msg3_key"]
        expected_values = ["msg1_value", "msg2_value", "msg3_value"]
        expected_partitions = [1, 2, 3]

        self.assertIn(message.key(), expected_keys)
        self.assertIn(message.value(payload=None), expected_values)
        self.assertIn(message.partition(), expected_partitions)

    @setup_kafka(topics=[{"topic": "edge_case_test", "partition": 16}])
    @produce(topic="edge_case_test", key="edge_key", value="edge_value", partition=0)
    @consume(topics=["edge_case_test"])
    def test_consume_decorator_edge_case_partition_zero(self, message):
        """
        Test case for edge case with partition 0.
        This ensures the fix works correctly even with partition 0,
        which can sometimes be a special case in Kafka implementations.
        """
        if message is None:
            return

        self.assertEqual(message.key(), "edge_key")
        self.assertEqual(message.value(payload=None), "edge_value")
        self.assertEqual(message.partition(), 0)

    @setup_kafka(topics=[{"topic": "signature_test", "partition": 16}])
    @produce(topic="signature_test", key="sig_key", value="sig_value", partition=5)
    @consume(topics=["signature_test"])
    def test_consume_decorator_function_signature_modification(self, message):
        """
        Test case to verify that the function works correctly with the signature modification.
        This test ensures that the decorator correctly handles the message parameter
        without causing pytest fixture issues.
        """
        if message is None:
            return

        self.assertEqual(message.key(), "sig_key")
        self.assertEqual(message.value(payload=None), "sig_value")
        self.assertEqual(message.partition(), 5)

    def test_signature_modification_verification(self):
        """
        Separate test to verify that the decorator modifies function signatures correctly.
        This test creates a decorated function and inspects its signature.
        """
        import inspect

        @consume(topics=["test_topic"])
        def test_function_for_signature(message):
            pass

        # Get the signature of the decorated function
        sig = inspect.signature(test_function_for_signature)

        # Verify that the message parameter exists
        message_param = sig.parameters.get('message')
        self.assertIsNotNone(message_param)

        # The test should pass if the default is not empty (even if it's None)
        # This prevents pytest from treating 'message' as a fixture
        self.assertNotEqual(message_param.default, inspect.Parameter.empty)

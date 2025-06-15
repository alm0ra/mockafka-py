"""
Test cases specifically for the pytest fixture issue fix in @consume decorator.

This module contains tests that reproduce and verify the fix for the issue where
pytest would treat function parameters without default values as fixtures,
causing 'fixture not found' errors when using the @consume decorator.

Issue: https://github.com/aiven/mockafka-py/issues/175
"""

from __future__ import annotations

import inspect
from unittest import TestCase

from mockafka import Message, consume, produce, setup_kafka


class TestPytestFixtureIssueFix(TestCase):
    """Test cases for the pytest fixture issue fix in @consume decorator."""

    def test_original_bug_report_example(self):
        """
        Test the exact example from the bug report.

        This test reproduces the original issue where the following code
        would fail with 'fixture message not found':

        @produce(topic='test', key='test_key', value='test_value', partition=4)
        @consume(topics=['test'])
        def test_function(message):  # No default value
            pass
        """

        @setup_kafka(topics=[{"topic": "bug_report_test", "partition": 16}])
        @produce(topic='bug_report_test', key=b'test_key', value=b'test_value', partition=4)
        @consume(topics=['bug_report_test'])
        def test_produce_and_consume_decorator(message):
            """
            This test showcases the usage of both @produce and @consume decorators in a single test case.
            It produces a message to the 'test' topic and then consumes it to perform further logic.
            # Notice you may get message None
            """
            if not message:
                return

            # Verify the message content
            self.assertEqual(message.key(), b'test_key')
            self.assertEqual(message.value(payload=None), b'test_value')
            self.assertEqual(message.partition(), 4)

        # This should not raise any pytest fixture errors
        test_produce_and_consume_decorator()

    def test_function_signature_modification(self):
        """
        Test that the @consume decorator properly modifies function signatures.

        The decorator should add default values to 'message' parameters that don't
        have them, preventing pytest from treating them as fixtures.
        """

        @consume(topics=['test_topic'])
        def test_function_no_default(message):
            pass

        @consume(topics=['test_topic'])
        def test_function_with_default(message=None):
            pass

        # Check that both functions now have default values for message parameter
        sig1 = inspect.signature(test_function_no_default)
        sig2 = inspect.signature(test_function_with_default)

        message_param1 = sig1.parameters.get('message')
        message_param2 = sig2.parameters.get('message')

        self.assertIsNotNone(message_param1)
        self.assertIsNotNone(message_param2)

        # Both should have default values now (not empty, even if None)
        self.assertNotEqual(message_param1.default, inspect.Parameter.empty)
        self.assertNotEqual(message_param2.default, inspect.Parameter.empty)

    def test_multiple_parameters_with_message(self):
        """
        Test that the decorator works correctly with functions that have
        multiple parameters, where only 'message' needs modification.
        """

        @consume(topics=['test_topic'])
        def test_function_multiple_params(self, message, other_param="default"):
            pass

        sig = inspect.signature(test_function_multiple_params)

        # Check that message parameter has default value
        message_param = sig.parameters.get('message')
        self.assertIsNotNone(message_param)
        self.assertNotEqual(message_param.default, inspect.Parameter.empty)

        # Check that other parameters are unchanged
        self_param = sig.parameters.get('self')
        other_param = sig.parameters.get('other_param')

        self.assertIsNotNone(self_param)
        self.assertIsNotNone(other_param)
        self.assertEqual(other_param.default, "default")

    def test_no_message_parameter(self):
        """
        Test that the decorator works correctly with functions that don't
        have a 'message' parameter at all.
        """

        @consume(topics=['test_topic'])
        def test_function_no_message_param(self, other_param):
            pass

        sig = inspect.signature(test_function_no_message_param)

        # Should not have a message parameter
        message_param = sig.parameters.get('message')
        self.assertIsNone(message_param)

        # Other parameters should be unchanged
        self_param = sig.parameters.get('self')
        other_param = sig.parameters.get('other_param')

        self.assertIsNotNone(self_param)
        self.assertIsNotNone(other_param)
        # other_param should not have a default value
        self.assertEqual(other_param.default, inspect.Parameter.empty)

    def test_backward_compatibility_with_existing_tests(self):
        """
        Test that the fix maintains backward compatibility with existing test patterns.

        This ensures that existing tests that already have default values continue to work.
        """

        @setup_kafka(topics=[{"topic": "compat_test", "partition": 16}])
        @produce(topic="compat_test", key=b"compat_key", value=b"compat_value", partition=1)
        @consume(topics=["compat_test"])
        def test_existing_pattern(message: Message | None = None):
            if message is None:
                return

            self.assertEqual(message.key(), b"compat_key")
            self.assertEqual(message.value(payload=None), b"compat_value")
            self.assertEqual(message.partition(), 1)

        # This should work without any issues
        test_existing_pattern()

    def test_edge_case_empty_function_signature(self):
        """
        Test edge case where function has no parameters at all.
        """

        @consume(topics=['test_topic'])
        def test_function_no_params():
            pass

        sig = inspect.signature(test_function_no_params)

        # Should have no parameters
        self.assertEqual(len(sig.parameters), 0)

    def test_complex_scenario_multiple_decorators(self):
        """
        Test complex scenario with multiple decorators and message consumption.

        This test ensures the fix works in realistic scenarios where multiple
        decorators are stacked together.
        """

        @setup_kafka(topics=[{"topic": "complex_test", "partition": 16}])
        @produce(topic="complex_test", key=b"key1", value=b"value1", partition=1)
        @produce(topic="complex_test", key=b"key2", value=b"value2", partition=2)
        @consume(topics=["complex_test"])
        def test_complex_scenario(message):
            if message is None:
                return

            # Should receive one of the two messages
            expected_data = [
                (b"key1", b"value1", 1),
                (b"key2", b"value2", 2)
            ]

            actual_data = (message.key(), message.value(payload=None), message.partition())
            self.assertIn(actual_data, expected_data)

        # This should work without pytest fixture errors
        test_complex_scenario()

    def test_function_with_args_and_kwargs(self):
        """
        Test that the decorator works with functions that use *args and **kwargs.
        """

        @consume(topics=['test_topic'])
        def test_function_with_varargs(message, *args, **kwargs):
            pass

        sig = inspect.signature(test_function_with_varargs)

        # Check that message parameter has default value
        message_param = sig.parameters.get('message')
        self.assertIsNotNone(message_param)
        self.assertNotEqual(message_param.default, inspect.Parameter.empty)

        # Check that *args and **kwargs are preserved
        params = list(sig.parameters.keys())
        self.assertIn('args', params)
        self.assertIn('kwargs', params)

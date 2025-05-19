import pytest
from mockafka import produce, consume, FakeConsumer


@produce(topic='test_topic', key='k', value='v', partition=0)
@consume(topics=['test_topic'])
def test_produce_and_consume_decorator(message):
    """Ensure @produce and @consume work together under pytest."""
    assert message.key() == 'k'
    assert message.value(payload=None) == 'v'


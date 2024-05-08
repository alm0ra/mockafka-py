from __future__ import annotations

from typing import Optional

from confluent_kafka import KafkaError


class Message:
    def __init__(self, *args, **kwargs):
        self._headers: Optional[dict] = kwargs.get("headers", None)
        self._key: Optional[str] = kwargs.get("key", None)
        self._value: Optional[str] = kwargs.get("value", None)
        self._topic: Optional[str] = kwargs.get("topic", None)
        self._offset: Optional[int] = kwargs.get("offset", None)
        self._error: Optional[KafkaError] = kwargs.get("error", None)
        self._latency: Optional[float] = kwargs.get("latency", None)
        self._leader_epoch: Optional[int] = kwargs.get("leader_epoch", None)
        self._partition: Optional[int] = kwargs.get("partition", None)
        self._timestamp: int = kwargs.get("timestamp", None)

    def offset(self, *args, **kwargs):
        return self._offset

    def latency(self, *args, **kwargs):
        return self._latency

    def leader_epoch(self, *args, **kwargs):
        return self._leader_epoch

    def headers(self, *args, **kwargs):
        return self._headers

    def key(self, *args, **kwargs):
        return self._key

    def value(self, *args, **kwargs):
        return self._value

    def timestamp(self, *args, **kwargs):
        return self._timestamp

    def topic(self, *args, **kwargs):
        return self._topic

    def partition(self, *args, **kwargs):
        return self._partition

    def error(self):
        return self._error

    def set_headers(self, *args, **kwargs):  # real signature unknown
        pass

    def set_key(self, *args, **kwargs):  # real signature unknown
        pass

    def set_value(self, *args, **kwargs):  # real signature unknown
        pass

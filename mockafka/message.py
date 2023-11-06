from typing import Optional

from confluent_kafka import KafkaError


class Message:
    def __init__(self, *args, **kwargs):
        self.headers: Optional[dict] = kwargs.get('headers', None)
        self.key: Optional[str] = kwargs.get('key', None)
        self.value: Optional[str] = kwargs.get('value', None)
        self.topic: Optional[str] = kwargs.get('topic', None)
        self.offset: Optional[int] = kwargs.get('offset', None)
        self.error: Optional[KafkaError] = kwargs.get('error', None)
        self.latency: Optional[float] = kwargs.get('latency', None)
        self.leader_epoch: Optional[int] = kwargs.get('leader_epoch', None)
        self.partition: Optional[int] = kwargs.get('partition', None)
        self.timestamp: int = kwargs.get('timestamp', None)

    def offset(self, *args, **kwargs):
        return self.offset

    def latency(self, *args, **kwargs):
        return self.latency

    def leader_epoch(self, *args, **kwargs):
        return self.leader_epoch

    def headers(self, *args, **kwargs):
        return self.headers

    def key(self, *args, **kwargs):
        return self.key

    def value(self, *args, **kwargs):
        return self.value

    def timestamp(self, *args, **kwargs):
        return self.timestamp

    def topic(self, *args, **kwargs):
        return self.topic

    def value(self, payload):
        return self.value

    def error(self):
        return self.error

    def set_headers(self, *args, **kwargs):  # real signature unknown
        pass

    def set_key(self, *args, **kwargs):  # real signature unknown
        pass

    def set_value(self, *args, **kwargs):  # real signature unknown
        pass

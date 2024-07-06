from __future__ import annotations

from typing import TypedDict
from typing_extensions import NotRequired


class MessageDict(TypedDict):
    value: NotRequired[str]
    key: NotRequired[str]
    topic: NotRequired[str]
    partition: NotRequired[int]
    timestamp: NotRequired[int]
    headers: NotRequired[dict]


class TopicConfig(TypedDict):
    topic: str
    partition: int

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

__all__ = ["ChatCreateCompletionParams", "Message"]


class ChatCreateCompletionParams(TypedDict, total=False):
    messages: Iterable[Message]

    model: str
    """Model being used. Currently ignored and defaults to "scholarai" with GPT4-turbo"""

    stream: bool
    """Whether or not to stream the response. Streaming is recommended!"""


class Message(TypedDict, total=False):
    content: str
    """Content of the message. Must be a string."""

    role: str
    """Role of the message. Must be "user" """

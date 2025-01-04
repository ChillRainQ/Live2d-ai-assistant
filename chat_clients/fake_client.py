from typing import Iterator

from core.abstract_chat_client import AbstractChatClient


class FakeClient(AbstractChatClient):
    def chat(self, message) -> str:
        return "这里是测试用TTS，非测试不要使用"

    def chat_iter(self, message: str) -> Iterator[str]:
        return self.chat(message)
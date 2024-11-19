from chat_clients.qwen_client import QwenClient
from config.application_config import ApplicationConfig
from core.abstract_chat_client import AbstractChatClient


class LLMFactory:
    @staticmethod
    def create(llm_name: str, **kwargs) -> AbstractChatClient | None:
        llm: AbstractChatClient | None
        if llm_name.lower() == 'fakellm':
            llm = None
        elif llm_name.lower() == 'qwen':
            llm = QwenClient(ApplicationConfig())
        else:
            raise ValueError(f'{llm_name} is not a valid LLM name.')
        print(f"现在使用的 LLM 为：{llm.__class__.__name__}")
        return llm


def test():
    instance = LLMFactory.create('fakellm')

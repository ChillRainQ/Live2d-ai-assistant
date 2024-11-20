import config.yaml_config_loader
from chat_clients.qwen_client import QwenClient
from core.abstract_chat_client import AbstractChatClient


class ChatClientFactory:
    llm: AbstractChatClient | None
    llm_configs: dict
    @staticmethod
    def create(llm_name: str) -> AbstractChatClient | None:
        llm_configs = config.yaml_config_loader.load_yaml_config(config.yaml_config_loader.CHAT_CLIENT_CONFIG)
        if llm_name.lower() == 'fakellm':
            llm = None
        elif llm_name.lower() == 'qwen':
            llm = QwenClient(config=llm_configs.get('qwen'))
        else:
            raise ValueError(f'{llm_name} is not a valid LLM name.')
        print(f"现在使用的 LLM 为：{llm.__class__.__name__}")
        return llm


def test():
    instance = ChatClientFactory.create('fakellm')

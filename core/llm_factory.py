import config.yaml_config_loader
from core.abstract_chat_client import AbstractChatClient
from core.gobal_components import i18n


class ChatClientFactory:
    llm: AbstractChatClient | None
    llm_configs: dict
    @staticmethod
    def create(llm_name: str) -> AbstractChatClient:
        llm_configs = config.yaml_config_loader.load_yaml_config(config.yaml_config_loader.CHAT_CLIENT_CONFIG)
        if llm_name.lower() == 'fake':
            from chat_clients.fake_client import FakeClient
            llm = FakeClient()
        elif llm_name.lower() == 'qwen':
            from chat_clients.qwen_client import QwenClient
            llm = QwenClient(config=llm_configs.get('qwen'))
        else:
            # core.llm_factory.create.valueError
            raise ValueError(f'{llm_name} {i18n.get_str("core.llm_factory.create.valueError")}')
        # core.llm_factory.create.llm_type
        print(f'{i18n.get_str("core.llm_factory.create.llm_type")}{llm.__class__.__name__}')
        return llm


def test():
    instance = ChatClientFactory.create('fakellm')

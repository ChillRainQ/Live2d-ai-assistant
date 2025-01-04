import config.yaml_config_loader
from core.abstract_tts_client import AbstractTTSClient
from core.gobal_components import i18n


class TTSClientFactory:
    tts_config: dict
    tts: AbstractTTSClient

    @staticmethod
    def create(tts_type: str, **kwargs) -> AbstractTTSClient:
        tts_config = config.yaml_config_loader.load_yaml_config(config.yaml_config_loader.TTS_CLIENT_CONFIG)
        if tts_type.lower() == 'cosyvoice':
            from tts_clients.cosyvoice_client import CosyVoiceClient
            tts = CosyVoiceClient(tts_config.get('cosyvoice'))
        elif tts_type.lower() == 'edgetts':
            from tts_clients.edge_tts_client import EdgeTTSClient
            tts = EdgeTTSClient(tts_config.get('edgetts'))
        elif tts_type.lower() == 'gptsovits':
            from tts_clients.gptsovits_client import GPTSovitsClient
            tts = GPTSovitsClient(tts_config.get('gptsovits'))
        else:
            pass
        # core.tts_factory.create.tts_type
        print(f'{i18n.get_str("core.tts_factory.create.tts_type")}{tts.type}')
        return tts

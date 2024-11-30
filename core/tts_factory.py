from core.abstract_tts_client import AbstractTTSClient
from tts_clients.cosyvoice_client import CosyVoiceClient
from tts_clients.edge_tts_client import EdgeTTSClient
import config.yaml_config_loader


class TTSClientFactory:
    tts_config: dict
    tts: AbstractTTSClient

    @staticmethod
    def create(tts_type: str, **kwargs) -> AbstractTTSClient:
        tts_config = config.yaml_config_loader.load_yaml_config(config.yaml_config_loader.TTS_CLIENT_CONFIG)
        if tts_type.lower() == 'cosyvoice':
            tts = CosyVoiceClient(tts_config.get('cosyvoice'))
        elif tts_type.lower() == 'edgetts':
            tts = EdgeTTSClient(tts_config.get('edgetts'))
        else:
            pass
        print(f'现在使用的 TTS 为：{tts.type}')
        return tts

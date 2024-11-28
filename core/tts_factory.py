from core.abstract_tts_client import AbstractTTSClient
from tts_clients.cosyvoice_client import CosyVoiceClient
from tts_clients.edge_tts_client import EdgeTTSClient


class TTSClientFactory:
    @staticmethod
    def create(tts_type: str, **kwargs) -> AbstractTTSClient:
        tts: AbstractTTSClient
        if tts_type.lower() == 'cosyvoice':
            tts = CosyVoiceClient("","")
        elif tts_type.lower() == 'edgetts':
            tts = EdgeTTSClient(
                voice=kwargs['system_prompt'].get('voice')
            )
        else:
            pass
        print(f'现在使用的 TTS 为：{tts.type}')
        return tts


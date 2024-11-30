import io
import os

import torch
import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav

from core.abstract_tts_client import AbstractTTSClient

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class CosyVoiceClient(AbstractTTSClient):
    def __init__(self, config: dict):
        self.type = 'cosyvoice'
        self.model = CosyVoice(config.get('model'))
        self.prompt_speech = load_wav(config.get('prompt_speech'), 16000)
        self.prompt_text = config.get('prompt_text').strip()

    async def generate_audio(self, text: str):
        audios = []
        for audio in self.model.inference_zero_shot(text, self.prompt_text, self.prompt_speech):
            audios.append(audio['tts_speech'])
        audio_bytes = io.BytesIO()
        torchaudio.save(audio_bytes, torch.concat(audios, dim=1), 22050, format='wav')
        audio_bytes.seek(0)
        return audio_bytes




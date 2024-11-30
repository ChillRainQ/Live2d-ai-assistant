import asyncio
import io
import os

import torchaudio

from config.application_config import ApplicationConfig
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
from utils import audio_player

from core.abstract_tts_client import AbstractTTSClient

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class CosyVoiceClient(AbstractTTSClient):
    def __init__(self, config: dict):
        self.type = 'cosyvoice'
        self.model = CosyVoice(config.get('model'))
        self.prompt_speech = load_wav(config.get('prompt_speech'), 16000)
        self.prompt_text = config.get('prompt_text').strip()

    async def generate_audio(self, text: str):
        audio = self.model.inference_zero_shot(text, self.prompt_text, self.prompt_speech)
        tts_speech = audio['tts_speech']
        audio_bytes = io.BytesIO()
        torchaudio.save(audio_bytes, tts_speech, 22050, format='wav')
        audio_bytes.seek(0)
        return audio_bytes

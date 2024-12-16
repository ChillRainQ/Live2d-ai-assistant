import io
import os

import numpy as np
import torch
import torchaudio

from core.audio_generator import AudioGenerator
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav

from core.abstract_tts_client import AbstractTTSClient
from utils.gobal_components import lock, audio_data, stop_event

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
dtype = np.float32

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

    def generate_audio_stream(self, text: str, audio_generate: AudioGenerator):
        global audio_data
        print('now generate_audio_stream')
        for i in self.model.inference_zero_shot(text, self.prompt_text, self.prompt_speech, stream=True):
            chunk = i['tts_speech'].numpy().astype(dtype).flatten()
            chunk = chunk.reshape(-1, 1)
            audio_generate.add(chunk)
            # with lock:
            #     if audio_data.size == 0:
            #         audio_data = chunk
            #     else:
            #         audio_data = np.concatenate((audio_data, chunk))  # 否则追加数据
        audio_generate.stop_event.set()





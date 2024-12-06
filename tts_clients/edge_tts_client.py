import asyncio
from io import BytesIO
from typing import Tuple

import edge_tts
import io

from pydub import AudioSegment

from config.application_config import ApplicationConfig
from core.abstract_tts_client import AbstractTTSClient


class EdgeTTSClient(AbstractTTSClient):


    def __init__(self, config: dict):
        self.type = 'edge_tts'
        self.model = None
        self.voice = config.get('voice')

    async def generate_audio(self, text: str) -> BytesIO:
        communicate = edge_tts.Communicate(text, self.voice)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_stream.seek(0)
        audio_bytes = AudioSegment.from_file(audio_stream, format='mp3')
        wav_stream = io.BytesIO()
        audio_bytes.export(wav_stream, format="wav")
        wav_stream.seek(0)
        return wav_stream

    def generate_audio_stream(self, text: str):
        return asyncio.run(self.generate_audio(text))
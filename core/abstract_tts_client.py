import abc
import io
import pickle

from core.audio_device import AudioPlayer
from core.audio_generator import AudioGenerator




class AbstractTTSClient(metaclass=abc.ABCMeta):
    audio_player: AudioPlayer()
    type: str
    model: object

    @abc.abstractmethod
    async def generate_audio(self, text: str):
        raise NotImplementedError

    @abc.abstractmethod
    def generate_audio_stream(self, text: str, audio_generate: AudioGenerator):
        raise NotImplementedError

    async def play_audio(self, audio_file: io.BytesIO):
        self.audio_player.play_audio(audio_file)

    def hook(self):
        pass


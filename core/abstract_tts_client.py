import abc
import io

from utils.audio_player import AudioPlayer


class AbstractTTSClient(metaclass=abc.ABCMeta):
    audio_player = AudioPlayer()
    type: str
    model: object

    @abc.abstractmethod
    async def generate_audio(self, text: str):
        raise NotImplementedError

    async def play_audio(self, audio_file: io.BytesIO):
        self.audio_player.play_audio(audio_file)

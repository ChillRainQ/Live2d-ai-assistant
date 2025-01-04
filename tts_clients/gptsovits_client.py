import io

from GPT_SoVITS_Refactor.cli.gptsovits_tts import GPTSovitsTTS
from core.abstract_tts_client import AbstractTTSClient
from GPT_SoVITS_Refactor.resources.configs.config import TTS_CONFIG
from core.audio_generator import AudioGenerator


class GPTSovitsClient(AbstractTTSClient):
    def generate_audio_stream(self, text: str, audio_generate: AudioGenerator):
        pass

    def __init__(self, config):
        super().__init__()
        self.type = "GPTSoVits"
        self.tts = GPTSovitsTTS(config=config)
        self.req = GPTSovitsTTS.TTS_Request(config=config)

    async def generate_audio(self, text: str):
        self.req.text = text
        audio, _ = self.tts.tts_handle(self.req)
        self.req.text = ""

        return audio


if __name__ == "__main__":
    client = GPTSovitsClient()
    audio = client.generate_audio("还有其他更快的么, 这个生成效果感觉最后也有概率会破音, 如何避免啊")

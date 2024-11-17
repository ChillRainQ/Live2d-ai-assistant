import asyncio
import io
import threading
import wave

import pyaudio
from pydub import AudioSegment
from pydub.utils import make_chunks


class AudioPlayer:
    """
    音频播放器
    """

    def __init__(self, chunk_len: int = 20):
        self.p = pyaudio.PyAudio()
        self.chunk_len = chunk_len

    def __get_volume_from_chunks(self, audio):
        """
        获取音量
        """
        chunks = make_chunks(audio, self.chunk_len)
        volumes = [chunk.rms for chunk in chunks]
        max_volume = max(volumes)
        if max_volume == 0:
            raise ValueError("最大音量为0！")
        return [volume / max_volume for volume in volumes]

    def prepare_audio(self, audio: str | io.BytesIO):
        """
        音频预处理
        支持文件路径和音频流(wav格式)
        """
        audio_file = io.BytesIO()
        # 如果输入是文件路径（不建议使用）
        if isinstance(audio, str):
            if audio.endswith('.wav'):
                audio_file = wave.open(audio, 'rb')
            elif audio.endswith('.mp3'):
                mp3_file = AudioSegment.from_file(audio, format='mp3')
                wav_data = io.BytesIO()
                mp3_file.export(wav_data, format='wav')
                wav_data.seek(0)
                audio_file = wave.open(wav_data, 'rb')
        # 如果输入是音频流（建议使用的方式）
        elif isinstance(audio, io.BytesIO):
            audio_bytes = AudioSegment.from_file(audio, format='wav')
            wav_data = audio_bytes.export(format='wav')
            wav_data.seek(0)
            audio_file = wave.open(wav_data, 'rb')
        else:
            raise TypeError("输入不是音频文件路径或音频流！")
        return audio_file

    # def play_audio(self, audio_file):
    #     stream = self.p.open(
    #         format=self.p.get_format_from_width(audio_file.getsampwidth()),
    #         channels=audio_file.getnchannels(),
    #         rate=audio_file.getframerate(),
    #         output=True,
    #     )
    #     data = audio_file.readframes(1024)
    #     while data:
    #         stream.write(data)
    #         data = audio_file.readframes(1024)
    #
    #     stream.stop_stream()
    #     stream.close()
    def play_audio(self, audio_file):
        # 通过线程播放音频
        def play():
            stream = self.p.open(
                format=self.p.get_format_from_width(audio_file.getsampwidth()),
                channels=audio_file.getnchannels(),
                rate=audio_file.getframerate(),
                output=True,
            )
            data = audio_file.readframes(1024)
            while data:
                stream.write(data)
                data = audio_file.readframes(1024)

            stream.stop_stream()
            stream.close()

        # 使用线程播放音频
        audio_thread = threading.Thread(target=play)
        audio_thread.start()

    async def async_play_audio(self, audio_file):
        stream = self.p.open(
            format=self.p.get_format_from_width(audio_file.getsampwidth()),
            channels=audio_file.getnchannels(),
            rate=audio_file.getframerate(),
            output=True,
        )
        data = audio_file.readframes(1024)
        while data:
            stream.write(data)
            data = audio_file.readframes(1024)

        stream.stop_stream()
        stream.close()


if __name__ == '__main__':
    p = AudioPlayer()
    # p.play_audio("D:\\PythonCode\\LLM-Assistant\\tts\\cache\\test.mp3")

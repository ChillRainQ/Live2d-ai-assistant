import io
import threading
import time
import wave
from abc import ABC, abstractmethod

import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks

from core.audio_generator import AudioGenerator
from utils.gobal_components import stop_event, lock


class AudioPlayer:
    """
    音频播放器
    """

    def __init__(self, chunk_len: int = 20):
        # self.p = pyaudio.PyAudio()
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

    def play_audio(self, audio_file: io.BytesIO):
        """
        常规音频播放
        """
        audio = AudioSegment.from_file(audio_file, format='wav')
        audio_data = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate
        sd.play(audio_data, sample_rate)
        sd.wait()

    def play_audio_stream(self, generator: AudioGenerator, play_front: callable = None, play_end: callable = None):
        # with sd.OutputStream(sample_rate=sample_rate,channels=1,
        #     dtype=dtype
        # ) as stream:
        #     for chunk in generator:
        #         if chunk.size > 0:
        #             if play_front:
        #                 play_front(chunk)
        #                 stream.write(chunk)
        #         else:
        #             time.sleep(0.01)
        #     if play_end:
        #         play_end()
        stream = None
        while not (generator.stop_event.is_set() and generator.queue.empty()):
            chunk = next(generator)
            if play_front is not None:
                threading.Thread(target=play_front, args=(chunk,), daemon=True).start()
            if stream is None or not stream.active:
                # 如果流未初始化或已停止，重新启动流
                stream = sd.OutputStream(
                    samplerate=22050,
                    channels=1,
                    dtype=np.float32
                )
                stream.start()
            stream.write(chunk)
        if play_end is not None:
            play_end()

        # global audio_data, stream
        # while not stop_event.is_set() or audio_data.size > 0:
        #     with lock:
        #         if audio_data.size > 0:
        #             if stream is None or not stream.active:
        #                 # 如果流未初始化或已停止，重新启动流
        #                 stream = sd.OutputStream(
        #                     samplerate=22050,
        #                     channels=1,
        #                     dtype=np.float32
        #                 )
        #                 stream.start()
        #             # 播放缓冲区中的音频
        #             data_to_play = audio_data.copy()  # 复制数据以避免数据竞争
        #             audio_data = np.array([], dtype=np.float32)  # 清空缓冲区
        #             stream.write(data_to_play)  # 异步写入数据
        #         else:
        #             time.sleep(0.01)

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

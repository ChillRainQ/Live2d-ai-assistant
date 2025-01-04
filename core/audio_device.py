import io
import threading

import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from pydub.utils import make_chunks

from core.audio_generator import AudioGenerator
from core.lock import Lockable


class AudioPlayer(Lockable):
    def __init__(self, chunk_len: int = 20):
        super().__init__()
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

    @Lockable.lock_decorator
    def play_audio(self, audio_file: io.BytesIO):
        """
        常规音频播放
        """
        if audio_file is None:
            return
        audio = AudioSegment.from_file(audio_file, format='wav')
        audio_data = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate
        sd.play(audio_data, sample_rate)
        sd.wait()

    @Lockable.lock_decorator
    def play_audio_stream(self, generator: AudioGenerator, play_front: callable = None, play_end: callable = None):
        stream = None
        print("now play audio stream mode")
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

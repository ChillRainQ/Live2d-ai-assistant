import io
import time
import wave

import numpy as np
from live2d.utils.lipsync import WavHandler
from live2d.utils.log import Info
from pydub import AudioSegment


class LocalWavHandler(WavHandler):
    """
    自定义WavHandler，原版只能提供文件路径，在此直接使用流
    """
    def __init__(self):
        super(LocalWavHandler, self).__init__()

    def Start(self, wav_stream: io.BytesIO):
        """
        io.BytesIO 为 wav 格式
        """
        wav_bytes = AudioSegment.from_file(wav_stream, format='wav')
        wav_data = wav_bytes.export(format='wav')
        wav_data.seek(0)
        print(type(wav_stream))
        self.ReleasePcmData()
        try:
            with wave.open(wav_data, "r") as wav:
                self.numFrames = wav.getnframes()
                self.sampleRate = wav.getframerate()
                self.sampleWidth = wav.getsampwidth()
                self.numChannels = wav.getnchannels()
                # 双声道 / 单声道
                self.pcmData = np.frombuffer(wav.readframes(self.numFrames), dtype=np.int16)
                # 标准化
                self.pcmData = self.pcmData / np.max(np.abs(self.pcmData))
                # 拆分通道
                self.pcmData = self.pcmData.reshape(-1, self.numChannels).T
                self.startTime = time.time()
                self.lastOffset = 0
        except Exception as e:
            Info(f"[LipSync]Failed to load wav file due to exception: {e}")
            self.ReleasePcmData()


    def Update(self) -> bool:
        return super().Update()


import threading

import numpy as np

from l2d.LocalWavHandler import LocalWavHandler
import queue
# 口型监控器
wav_handler = LocalWavHandler()
# 流式音频队列
audio_stream = queue.Queue()
# 流式音频np数组
audio_data = np.array([], dtype=np.float32)
# 流式音频lock
lock = threading.Lock()
# 流式音频播放控制
stop_event = threading.Event()
# 音频流对象
stream = None
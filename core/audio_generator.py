import queue
import threading
import time

import numpy as np


class AudioGenerator:
    """
    音频迭代器，用于对流式播放的支持
    """
    def __init__(self, sample_rate=22050, dtype=np.float32):
        self.queue = queue.Queue(maxsize=100)
        self.sample_rate = sample_rate
        self.dtype = dtype
        self.stop_event = threading.Event()

    def add(self, chunk):
        self.queue.put(chunk)

    def complete(self):
        self.stop_event.set()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if not (self.stop_event.is_set() and self.queue.empty()):
                try:
                    return self.queue.get()
                except queue.Empty:
                    time.sleep(0.01)
            raise StopIteration("音频迭代器发生错误！")

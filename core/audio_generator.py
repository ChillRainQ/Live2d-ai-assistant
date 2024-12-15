import queue
import threading

import numpy as np


class AudioGenerator:
    """
    音频迭代器，用于对流式播放的支持
    """

    def __init__(self, sample_rate=22050, dtype=np.float32):
        self.queue = queue.Queue(maxsize=100)
        self.stop_event = threading.Event()

    def add(self, chunk):
        self.queue.put(chunk)

    def complete(self):
        self.stop_event.set()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stop_event.is_set() or self.queue.empty():
            try:
                return self.queue.get(timeout=0.1)
            except queue.Empty:
                pass
        raise StopIteration

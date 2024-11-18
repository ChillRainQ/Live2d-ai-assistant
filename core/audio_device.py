from PySide6.QtMultimedia import QMediaPlayer

from core.lock import Lockable
class AudioPlayer(Lockable):

    @staticmethod
    def lock_decorator(func):
        return super().lock_decorator(func)

    def is_locked(self) -> bool:
        return super().is_locked()

    def unlock(self):
        super().unlock()

    def lock(self):
        super().lock()

    def __init__(self, onFinishCallback: callable):
        self.finished = True
        self.onFinishCallback = onFinishCallback
        self.audioPlayer = QMediaPlayer()
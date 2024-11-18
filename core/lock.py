class Lockable:
    _locked: bool
    def __init__(self):
        self._locked = False

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def is_locked(self) -> bool:
        return self._locked


    @staticmethod
    def lock_decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.is_locked():
                return
            return func(self, *args, **kwargs)
        return wrapper

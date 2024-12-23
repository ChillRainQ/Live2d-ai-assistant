from qfluentwidgets import TeachingTip, TeachingTipTailPosition, TeachingTipView

from core.lock import Lockable

"""
文本弹出框
"""


class PopText(Lockable):
    currentTip: TeachingTip | None

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.currentTip = None

    @Lockable.lock_decorator
    def pop(self, text: str, title: str = "") -> None:
        view = TeachingTipView(
            icon=None,
            title=title,
            content=text,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
        )
        self.currentTip = TeachingTip.make(
            target=self.target,
            view=view,
            duration=-1,
            parent=self.target,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            isDeleteOnClose=True,
        )
        view.closed.connect(self.__closePopText)

    @Lockable.lock_decorator
    def fadeOut(self):
        if self.currentTip is not None:
            self.__closePopText()

    def __closePopText(self):
        self.currentTip.close()
        self.currentTip = None
        print("text pop finished")

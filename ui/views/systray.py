from abc import ABC, abstractmethod

from PySide6.QtGui import QAction, QCursor, QIcon
from PySide6.QtWidgets import QSystemTrayIcon
from qfluentwidgets import CheckableMenu

from config.application_config import ApplicationConfig


class SysTrayIcon(QSystemTrayIcon):
    """
    托盘图标
    """

    class CallbackSet(ABC):
        @abstractmethod
        def trayDoubleClicked(self):
            pass

        @abstractmethod
        def exitApplication(self):
            pass

        @abstractmethod
        def displayCharactor(self):
            pass

        @abstractmethod
        def openSettings(self):
            pass

        @abstractmethod
        def setStayOnTop(self):
            pass

        @abstractmethod
        def exitApplication(self):
            pass

        @abstractmethod
        def clickPenetrate(self):
            pass
    action_ls: list
    config: ApplicationConfig
    callbackSet: CallbackSet

    def __init__(self):
        super().__init__()
        self.action_ls = [
            QAction("显示角色"),
            QAction("角色置顶"),
            QAction("鼠标穿透"),
            QAction("打开设置"),
            QAction("退出"),
        ]

        menu = CheckableMenu()
        menu.addActions(self.action_ls[:-1])
        menu.addSeparator()
        menu.addAction(self.action_ls[-1])
        self.setContextMenu(menu)



    def signalConnectSlot(self):
        self.activated.connect(self.activatedAction)

    def setup(self, config: ApplicationConfig, callbackSet: CallbackSet):
        self.config = config
        self.setIcon(QIcon(self.config.icon.value))
        self.callbackSet = callbackSet
        self.setToolTip("Live2d AI Assistant")

        functions = [
            self.callbackSet.displayCharactor,
            self.callbackSet.setStayOnTop,
            self.callbackSet.clickPenetrate,
            self.callbackSet.openSettings,
            self.callbackSet.exitApplication,
        ]
        values = [
            self.config.visible.value,
            self.config.stay_on_top.value,
            self.config.clickPenetrate.value,
            None,
            None,
        ]

        for idx, action in enumerate(self.action_ls):
            if values[idx] is not None:
                action.setCheckable(True)
                action.setChecked(values[idx])
            action.triggered.connect(functions[idx])
        self.signalConnectSlot()

    def start(self):
        self.show()

    def activatedAction(self, reason):
        """
        托盘动作
        """
        if reason == self.ActivationReason.Context:
            print(self.contextMenu().sizeHint().height(), " menu")
            self.contextMenu().move(QCursor.pos().x(), QCursor.pos().y() - self.contextMenu().height())
            self.contextMenu().show()

        if reason == self.ActivationReason.DoubleClick:
            self.callbackSet.trayDoubleClicked()

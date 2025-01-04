import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from qfluentwidgets import SplashScreen
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
from qframelesswindow import StandardTitleBar

from config.application_config import ApplicationConfig
import resources.resource as resource


class StartScene(FramelessWindow):
    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.resize(config.width.value, config.height.value)
        self.move(config.lastX.value, config.lastY.value)
        self.setWindowIcon(QIcon(os.path.join(resource.RESOURCE_DIR, "icon.png")))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(250, 250))
        self.titleBar.maxBtn.hide()
        self.titleBar.minBtn.hide()
        self.titleBar.closeBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.titleBar = StandardTitleBar(self.splashScreen)
        self.titleBar.setIcon(self.windowIcon())
        self.setTitleBar(self.titleBar)
        # self.splashScreen.setTitleBar(self.titleBar)
        self.show()


    def close(self):
        print("start scene close......")
        self.splashScreen.finish()
        self.hide()

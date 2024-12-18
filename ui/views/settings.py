import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon

from config.application_config import ApplicationConfig
from ui.components.settings.application_setting import ApplicationSetting


class Settings(FluentWindow):
    application_setting: ApplicationSetting
    config: ApplicationConfig
    resource_dir: str

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.config = config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.application_setting = ApplicationSetting(self.config)
        self.addSubInterface(self.application_setting, FluentIcon.APPLICATION, "应用设置")
        self.addSubInterface(self.application_setting, FluentIcon.APPLICATION, "应用设置2")
        self.addSubInterface(self.application_setting, FluentIcon.APPLICATION, "应用设置3")
        self.addSubInterface(self.application_setting, FluentIcon.APPLICATION, "应用设置4")
        self.setMinimumSize(700, 500)

    def setup(self, config: ApplicationConfig):

        self.resource_dir = config.resource_dir.value

    def show(self):
        self.hide()
        size = QApplication.primaryScreen().size()
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        self.setVisible(True)
        self.adjustSize()
        self.setMicaEffectEnabled(True)

    def icon(self, path: str):
        return QIcon(os.path.join(self.resource_dir.rsplit("/", maxsplit=1)[0], path))
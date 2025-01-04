import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon, setTheme, Theme, NavigationItemPosition

from config.application_config import ApplicationConfig
from core.gobal_components import i18n
from ui.components.appSettingWidget import AppSettingWidget
from ui.components.consoleWidget import ConsoleWidget
from ui.components.settings.ai_setting import AiSetting
from ui.components.settings.application_setting import SceneShowSetting


class Settings(FluentWindow):
    scene_setting: SceneShowSetting
    config: ApplicationConfig
    resource_dir: str

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        setTheme(Theme.AUTO)
        self.setWindowTitle(f'{i18n.get_str("application.systray.title")}')
        self.setWindowIcon(QIcon('resources/icon.png'))
        self.config = config
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.scene_setting = SceneShowSetting(self.config)
        self.ai_setting = AiSetting(self.config)
        self.app_setting = AppSettingWidget(self.config)
        self.console_output = ConsoleWidget(self.config)
        self.addSubInterface(self.scene_setting, FluentIcon.APPLICATION, f'显示设置')
        self.addSubInterface(self.ai_setting, FluentIcon.CHAT, 'AI设置')

        self.addSubInterface(self.console_output, FluentIcon.COMMAND_PROMPT, '控制台', position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.app_setting, FluentIcon.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        self.setMinimumSize(700, 500)
        self.resource_dir = self.config.resource_dir.value
        self.updateFrameless()
        self.setMicaEffectEnabled(True)


    def setup(self, callback: AiSetting.CallBackSet):
        # 移除最大化按钮
        self.ai_setting.setup(callback)
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        # sys.stdout = self.console_output
        # sys.stderr = self.console_output
        # self.config.language.valueChanged.connect()

    def flash(self):
        self.scene_setting = SceneShowSetting(self.config)


    def show(self):
        self.hide()
        size = QApplication.primaryScreen().size()
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        self.setVisible(True)
        self.adjustSize()


    def icon(self, path: str):
        return QIcon(os.path.join(self.resource_dir.rsplit("/", maxsplit=1)[0], path))
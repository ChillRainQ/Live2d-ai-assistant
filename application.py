import sys
import live2d.v3 as live2d

from PySide6.QtWidgets import QApplication

from config.application_config import ApplicationConfig
from l2d.l2d_model import Live2DModel
from ui.views.l2d_scene import Live2DScene
from ui.views.systray import SysTrayIcon


class Application(
    Live2DModel.CallbackSet,
    SysTrayIcon.CallbackSet
):
    def onPlayText(self, group: str, no: int):
        pass

    def onPlaySound(self, group: str, no: int):
        pass

    def onMotionSoundFinished(self):
        pass

    def isSoundFinished(self) -> bool:
        pass

    def onChatOpen(self):
        pass

    def trayDoubleClicked(self):
        self.scene.activateWindow()

    def setStayOnTop(self):
        self.config.stay_on_top.value = not self.config.stay_on_top.value
        self.scene.show()

    def exitApplication(self):
        self.exit()

    def displayCharactor(self):
        self.config.visible.value = not self.config.visible.value
        self.scene.show()

    def clickPenetrate(self):
        self.config.clickPenetrate.value = not self.config.clickPenetrate.value
        self.scene.show()

    app: QApplication
    config: ApplicationConfig

    def __init__(self):
        self.app = QApplication()
        self.config = ApplicationConfig()
        self.scene = Live2DScene()
        # self.audio_player =
        self.l2d_model = Live2DModel()
        self.systray = SysTrayIcon()

    def load_config(self):
        """
        加载配置
        """
        pass

    def setup(self):
        """
        设置应用程序
        """
        live2d.init()
        self.l2d_model.setup(self.config, self)
        self.scene.setup(self.config, self.l2d_model)
        self.systray.setup(self.config, self)

    def start(self):
        """
        启动
        """
        self.scene.start()
        self.systray.start()
        self.app.exec()

    def exit(self):
        """
        退出操作
        """
        self.app.exit()
        sys.exit()


if __name__ == '__main__':
    print("application init....")
    app = Application()
    print("load config....")
    app.load_config()
    print("setup app....")
    app.setup()
    print("run app....")
    app.start()

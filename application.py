import asyncio
import io
import sys
import threading

import live2d.v3 as live2d

from PySide6.QtWidgets import QApplication
from live2d.v3.params import StandardParams

from config.application_config import ApplicationConfig
from l2d.l2d_model import Live2DModel
from tts.tts_factory import TTSFactory
from tts.tts_interface import TTSInterface
from utils import queues
from llm.llm_interface import LLMInterface
from ui.views.flyout_chatbox import FlyoutChatBox
from ui.views.l2d_scene import Live2DScene
from ui.views.systray import SysTrayIcon
from utils.gobal_components import wav_handler


class Application(
    Live2DModel.CallbackSet,
    SysTrayIcon.CallbackSet
):
    def onPlayText(self, group: str, no: int):
        pass

    def onPlaySound(self, group: str, no: int, audio_wav: io.BytesIO = None):
        if audio_wav:
            # 确保音频数据是BytesIO对象
            audio = self.l2d_model.audioPlayer.prepare_audio(audio_wav)
            # threading.Thread(target=self.audio_player.play_audio(audio)).start()
            self.l2d_model.audioPlayer.play_audio(audio)
            print("语音播放完成")
            # asyncio.run(self.audio_player.async_play_audio(audio))
            wav_handler.Start(audio_wav)
            print("口型同步已设定")
            if wav_handler.Update():
                # 设置模型口型
                print('尝试口型同步')
                print(f'响度：{wav_handler.GetRms()}')
                self.l2d_model.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                                       wav_handler.GetRms() * 1.0, 1)
        else:
            print("没有音频数据可播放")

    def onMotionSoundFinished(self):
        pass

    def isSoundFinished(self) -> bool:
        pass

    def onChatOpen(self):
        self.chatBox.show()

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
    chatBox: FlyoutChatBox
    llm: LLMInterface
    tts: TTSInterface

    def __init__(self, config: ApplicationConfig):
        self.app = QApplication()
        self.config = config
        self.scene = Live2DScene()
        self.tts = TTSFactory.create(self.config.tts_type.value, system_prompt={
            'voice': self.config.edge_voice.value
        })
        self.chatBox = FlyoutChatBox(self.scene)
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
        self.chatBox.setup(self.config)

        # self.chatBox.sent.connect(self.sendMessage)
        self.chatBox.sendMessageSignal.connect(self.sendMessage)

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
        live2d.dispose()
        self.app.exit()
        sys.exit()

    def sendMessage(self, text: str):
        """
        消息队列添加输入的消息
        """
        queues.send_queue.put(text)
        msg = queues.getMsg_queue.get()
        threading.Thread(target=self.say, args=(msg,), daemon=True).start()
    def say(self, msg):
        audio = asyncio.run(self.tts.generate_audio(msg))
        self.l2d_model.startOnMotionHandler("group", "no", audio)


if __name__ == '__main__':
    print("application init....")
    config = ApplicationConfig()
    app = Application(config)
    print("load config....")
    app.load_config()
    print("setup app....")
    app.setup()
    print("run app....")
    app.start()

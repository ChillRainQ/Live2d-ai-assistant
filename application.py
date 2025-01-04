import asyncio
import atexit
import io
import os
import sys
import threading
import time
import wave

import numpy as np
from PySide6.QtGui import Qt
from qfluentwidgets import qconfig, InfoBar, InfoBarPosition, FluentTranslator

import live2d.v3 as live2d
from PySide6.QtCore import QTimer, Signal, QObject

from PySide6.QtWidgets import QApplication

from core.audio_device import AudioPlayer
from core.audio_generator import AudioGenerator
from core.lock import Lockable
from live2d.v3.params import StandardParams

from config.application_config import ApplicationConfig
from core.abstract_tts_client import AbstractTTSClient
from core.filter import Filter
from core.tts_factory import TTSClientFactory
from prompts import prompts_loader
from core.abstract_chat_client import AbstractChatClient
from core.llm_factory import ChatClientFactory
from l2d.l2d_model import Live2DModel

from ui.components.popText import PopText
from ui.components.settings.ai_setting import AiSetting
from ui.views.flyout_chatbox import FlyoutChatBox
from ui.views.l2d_scene import Live2DScene
from ui.views.settings import Settings
from ui.views.systray import SysTrayIcon
from core.gobal_components import wav_handler, i18n

APP_PATH = os.path.dirname(__name__)


class Signals(QObject):
    llm_callback_signal = Signal(str, io.BytesIO, AudioGenerator)


class Application(
    Live2DModel.CallbackSet,
    SysTrayIcon.CallbackSet,
    AiSetting.CallBackSet,
):
    def onPlayText(self, group: str, no: int):
        pass

    def onPlaySound(self, group: str, no: int, audio_wav: io.BytesIO | AudioGenerator):
        stream = self.config.tts_stream.value
        if isinstance(audio_wav, io.BytesIO) and not stream:
            # application.onPlaySound.playMode.default
            print(f'{i18n.get_str("application.onPlaySound.playMode.default")}')
            self._playAudioAndSync(audio_wav)
        elif isinstance(audio_wav, AudioGenerator) and stream:
            # application.onPlaySound.playMode.stream
            print(f'{i18n.get_str("application.onPlaySound.playMode.stream")}')
            self._playAudioStreamAndSync(audio_wav)
        else:
            # application.onPlaySound.playMode.none
            print(f'{i18n.get_str("application.onPlaySound.playMode.none")}')

    def _playAudioAndSync(self, audio_wav: io.BytesIO):
        """
        常规音频播放
        """
        # application.playAudioAndSync.play.default
        print(f'{i18n.get_str("application.playAudioAndSync.play.default")}')
        if audio_wav is None:
            return
        # application.playAudioAndSync.play.done
        print(f'{i18n.get_str("application.playAudioAndSync.play.done")}')
        wav_handler.Start(audio_wav)
        # application.playAudioAndSync.setMouthSync
        print(f'{i18n.get_str("application.setMouthSync.done")}')
        if wav_handler.Update():
            threading.Thread(target=self.audioPlayer.play_audio, args=(audio_wav,)).start()
            # 设置模型口型
            # application.setMouthSync.done
            print(f'{i18n.get_str("application.setMouthSync.done")}')
            # application.setMouthSync.wav
            print(f'{i18n.get_str("application.setMouthSync.wav")}{wav_handler.GetRms()}')
            time.sleep(0.5)
            self.l2d_model.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                                   wav_handler.GetRms() * 1.0, 1)

    def _playAudioStreamAndSync(self, audio_generate: AudioGenerator):
        # todo 流式音频播放
        """
        流式音频播放
        当前问题： 1.没有播放音频
                2.瞬间完成执行（弹出了对话框）
        """
        # application.playAudioStreamAndSync.play.stream
        print(f'{i18n.get_str("application.playAudioStreamAndSync.play.stream")}')

        def play_front(chunk: np.ndarray):
            if chunk.dtype == np.float32:
                np_array = np.int16(chunk * 32767)
            else:
                # application.playAudioStreamAndSync.play_front.typeError
                raise TypeError(f'{i18n.get_str("application.playAudioStreamAndSync.play_front.typeError")}')
            wav = io.BytesIO()
            with wave.open(wav, 'wb') as file:
                file.setnchannels(1)  # 单声道
                file.setsampwidth(2)  # 2 字节（16 位）
                file.setframerate(22050)  # 设置采样率
                file.writeframes(np_array.tobytes())
            wav.seek(0)
            wav_handler.Start(wav)
            if wav_handler.Update():
                # 设置模型口型
                # application.setMouthSync.done
                print(f'{i18n.get_str("application.setMouthSync.done")}')
                # application.setMouthSync.wav
                print(f'{i18n.get_str("application.setMouthSync.wav")}{wav_handler.GetRms()}')
                self.l2d_model.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                                       wav_handler.GetRms() * 1.0, 1)

        # application.playAudioStreamAndSync.play.start
        print(f'{i18n.get_str("application.playAudioStreamAndSync.play.start")}')
        threading.Thread(target=self.audioPlayer.play_audio_stream, args=(audio_generate, play_front, None,),
                         daemon=True).start()

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

    def openSettings(self):
        self.setting.show()

    def flash_llm(self):
        def flash():
            del self.llm
            self.llm = ChatClientFactory.create(self.config.llm_type.value)

        flash()
        InfoBar.success(
            title='Success!',
            content=f'已修改为：{self.llm.__class__.__name__}',
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self.setting
        )

    def flash_tts(self):
        def flash():
            del self.tts
            self.tts = TTSClientFactory.create(self.config.tts_type.value)

        flash()
        InfoBar.success(
            title='Success!',
            content=f'已修改为：{self.tts.__class__.__name__}',
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self.setting
        )

    app: QApplication
    config: ApplicationConfig
    chatBox: FlyoutChatBox
    llm: AbstractChatClient
    tts: AbstractTTSClient
    audioPlayer: AudioPlayer | None
    signals: Signals
    setting: Settings
    chat_filter: Filter
    popText: PopText

    def __init__(self, config: ApplicationConfig):
        super().__init__()
        self.app = QApplication()
        self.config = config
        self.scene = Live2DScene()
        self.audioPlayer = AudioPlayer()
        self.chatBox = FlyoutChatBox(self.scene)
        self.l2d_model = Live2DModel()
        self.systray = SysTrayIcon()
        self.setting = Settings(self.config)
        self.signals = Signals()
        self.lock = False

    def load_config(self):
        """
        加载配置
        """

        self.config.llm_prompts = prompts_loader.get_personalities_list()

    def setup(self):
        """
        设置应用程序
        """
        atexit.register(self.save)
        live2d.init()
        self.llm = ChatClientFactory.create(self.config.llm_type.value)
        self.tts = TTSClientFactory.create(self.config.tts_type.value)
        self.config.setup()
        self.l2d_model.setup(self.config, self)
        self.scene.setup(self.config, self.l2d_model)
        self.systray.setup(self.config, self)
        self.chatBox.setup(self.config)
        self.setting.setup(self)
        self.popText = PopText(self.scene)
        self.signalConnectSlot()

    def signalConnectSlot(self):
        self.chatBox.sendMessageSignal.connect(self.chat)
        self.signals.llm_callback_signal.connect(self.chatCallback)

    def start(self):
        """
        启动
        """
        self.scene.start()
        self.systray.start()
        translator = FluentTranslator()
        self.app.installTranslator(translator)
        self.app.exec()

    def save(self) -> None:
        """
        保存配置
        """
        self.config.save()
        print(f'{i18n.get_str("application.save.done")}')

    def exit(self):
        """
        退出操作
        """
        live2d.dispose()
        self.app.exit()
        sys.exit()

    def chat(self, text: str):
        """
        聊天任务
        """
        self.chatBox.disable()
        self.popText.fadeOut()
        self.popText.lock()
        threading.Thread(target=self.chatMotion, args=(text,), daemon=True).start()

    def chatMotion(self, text):
        """
        开始一个 chat 动作
        """
        try:
            now = time.time()
            response = self.llm.chat(text)
            # application.chatMotion.responseTime
            print(f'{i18n.get_str("application.chatMotion.responseTime")}{time.time() - now}')
            now = time.time()
            if self.config.tts_stream.value:
                # application.chatMotion.audio.mode.stream
                print(f'{i18n.get_str("application.chatMotion.audio.mode.stream")}')

                audio_generate = AudioGenerator()
                # 子线程流式生成音频
                threading.Thread(target=self.tts.generate_audio_stream, args=(response, audio_generate,),
                                 daemon=True).start()
                self.signals.llm_callback_signal.emit(response, None, audio_generate)
            else:
                # application.audio.mode.default
                print(f'{i18n.get_str("application.audio.mode.default")}')
                audio = asyncio.run(self.tts.generate_audio(response))
                # application.chatMotion.audio.time
                print(f'{i18n.get_str("application.chatMotion.audio.time")}{time.time() - now}')
                self.signals.llm_callback_signal.emit(response, audio, None)
        finally:
            self.chatBox.enable()
            self.popText.fadeOut()
            self.popText.unlock()

    def chatCallback(self, msg: str, audio_io: io.BytesIO, audio_generator: AudioGenerator):
        """
        llm 返回响应回调
        audio_io: 音频ioByte,对应默认生成
        audio_generator: 自定义音频迭代器，对应流式生成
        """
        # application.chatCallback.start
        print(f'{i18n.get_str("application.chatCallback.start")}')
        audio = None
        if audio_io is not None:
            audio = audio_io
        elif audio_generator is not None:
            audio = audio_generator
        self.l2d_model.startChatMotion(live2d.MotionGroup.IDLE.value, live2d.MotionPriority.IDLE.value, audio)
        self.popText.fadeOut()
        self.popText.unlock()
        self.popText.pop(msg)
        timer = QTimer(self.popText.currentTip)
        timer.timeout.connect(self.popText.fadeOut)
        timer.start(500 * len(msg))


if __name__ == '__main__':
    # application.main.init
    print("application init....")
    config = ApplicationConfig()
    app = Application(config)
    # application.main.loadConfig
    print("load config....")
    app.load_config()
    # application.main.setupApp
    print("setup app....")
    app.setup()
    # application.main.runApp
    print("run app....")
    app.start()

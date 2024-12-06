import asyncio
import io
import os
import sys
import threading
import time

import numpy as np
import torch
import torchaudio

import live2d.v3 as live2d
from PySide6.QtCore import QTimer, Signal, QObject

from PySide6.QtWidgets import QApplication

import utils.gobal_components
from live2d.v3.params import StandardParams
import sounddevice as sd

from config.application_config import ApplicationConfig
from core.abstract_tts_client import AbstractTTSClient
from core.filter import Filter
from core.tts_factory import TTSClientFactory
from prompts import prompts_loader
from core.abstract_chat_client import AbstractChatClient
from core.llm_factory import ChatClientFactory
from l2d.l2d_model import Live2DModel

from ui.components.popText import PopText
from ui.views.flyout_chatbox import FlyoutChatBox
from ui.views.l2d_scene import Live2DScene
from ui.views.settings import Settings
from ui.views.systray import SysTrayIcon
from utils import audio_player
from utils.gobal_components import wav_handler
from utils.gobal_components import stop_event, lock
APP_PATH = os.path.dirname(__name__)

class Signals(QObject):
    llm_callback_signal = Signal(str, io.BytesIO)


class Application(
    Live2DModel.CallbackSet,
    SysTrayIcon.CallbackSet
):
    def onPlayText(self, group: str, no: int):
        pass

    def onPlaySound(self, group: str, no: int, audio_wav: io.BytesIO = None):
        stream = self.config.tts_stream.value
        if audio_wav and not stream:
            # 直接播放
            print('default mode')
            self._playAudioAndSync(audio_wav)
        elif stream and utils.gobal_components.audio_data.size > 0:
            # 流式音频播放
            print("stream mode")
            self._playAudioStreamAndSync()
        else:
            print("没有音频数据可播放")


    def _playAudioAndSync(self, audio_wav: io.BytesIO = None):
        """
        常规音频播放
        """
        threading.Thread(target=self.audioPlayer.play_audio, args=(audio_wav,)).start()
        print("语音播放完成")
        wav_handler.Start(audio_wav)
        print("口型同步已设定")
        if wav_handler.Update():
            # 设置模型口型
            print('尝试口型同步')
            print(f'响度：{wav_handler.GetRms()}')
            self.l2d_model.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                                   wav_handler.GetRms() * 1.0, 1)

    def _playAudioStreamAndSync(self):
        """
        流式音频播放
        """
        def play_audio_stream():
            print(1)
            global audio_data, stream
            while not stop_event.is_set() or audio_data.size > 0:
                with lock:
                    if audio_data.size > 0:
                        if stream is None or not stream.active:
                            # 如果流未初始化或已停止，重新启动流
                            stream = sd.OutputStream(
                                samplerate=22050,
                                channels=1,
                                dtype=np.float32
                            )
                            stream.start()
                        # 播放缓冲区中的音频
                        audio_buffer_stream = io.BytesIO()
                        data_to_play = audio_data.copy()  # 复制数据以避免数据竞争
                        audio_data = np.array([], dtype=np.float32)  # 清空缓冲区
                        stream.write(data_to_play) # 异步写入数据
                        audio_buffer_stream.seek(0)  # 将指针移到开头
                        audio_buffer_stream.write(data_to_play.tobytes())
                        def update(audio_wav):
                            print(2)
                            wav_handler.Start(audio_wav)
                            print("口型同步已设定")
                            if wav_handler.Update():
                                # 设置模型口型
                                print('尝试口型同步')
                                print(f'响度：{wav_handler.GetRms()}')
                                self.l2d_model.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                                                       wav_handler.GetRms() * 1.0, 1)
                        threading.Thread(target=update, args=(audio_buffer_stream,)).start()
                    else:
                        time.sleep(0.01)
        threading.Thread(target=play_audio_stream).start()
        print(3)
        print("开始流式播放")


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

    app: QApplication
    config: ApplicationConfig
    chatBox: FlyoutChatBox
    llm: AbstractChatClient
    tts: AbstractTTSClient
    audioPlayer: audio_player.AudioPlayer | None
    signals: Signals
    setting: Settings
    chat_filter: Filter
    popText: PopText

    def __init__(self, config: ApplicationConfig):
        self.app = QApplication()
        self.config = config
        self.scene = Live2DScene()
        self.audioPlayer = audio_player.AudioPlayer()
        self.chatBox = FlyoutChatBox(self.scene)
        self.l2d_model = Live2DModel()
        self.systray = SysTrayIcon()
        self.setting = Settings(self.config)
        self.signals = Signals()

    def load_config(self):
        """
        加载配置
        """
        self.config.llm_prompts = prompts_loader.get_personalities_list()

    def setup(self):
        """
        设置应用程序
        """
        live2d.init()
        self.llm = ChatClientFactory.create(self.config.llm_type.value)
        self.tts = TTSClientFactory.create(self.config.tts_type.value)
        self.l2d_model.setup(self.config, self)
        self.scene.setup(self.config, self.l2d_model)
        self.systray.setup(self.config, self)
        self.chatBox.setup(self.config)
        self.setting.setup(self.config)
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
        self.app.exec()

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
        threading.Thread(target=self.chatMontion, args=(text,), daemon=True).start()

    def chatMontion(self, text):
        """
        开始一个 chat 动作
        """
        try:
            now = time.time()
            response = self.llm.chat(text)
            print(f"response time：{time.time() - now}")
            now = time.time()
            # todo 支持流式生成音频，并且可以口型同步
            if self.config.tts_stream.value:
                global stop_event, lock, audio_data
                print("generate audio by stream mode")
                # 子线程生成音频
                with lock:
                    audio_data = np.array([], dtype=np.float32)
                stop_event.clear()
                threading.Thread(target=self.tts.generate_audio_stream, args=(response,), daemon=True).start()
                while not utils.gobal_components.audio_data.size > 0:
                    pass
                self.signals.llm_callback_signal.emit(response, None)
                """
                                    音频转换为BytesIO
                                    lock
                                    子线程播放
                                    口型同步
                                    unlock 使用锁定的方式或者使用消息队列，音频生成完成后直接丢队列，另一边一直取，直到收到结束   
                                    """
            else:
                print("generate audio by default mode")
                audio = asyncio.run(self.tts.generate_audio(response))
                print(f"audio time：{time.time() - now}")
                self.signals.llm_callback_signal.emit(response, audio)
        finally:
            self.chatBox.enable()
            self.popText.fadeOut()
            self.popText.unlock()

    def chatCallback(self, msg, audio):
        """
        llm 返回响应回调
        """
        self.l2d_model.startChatMotion(live2d.MotionGroup.IDLE.value, live2d.MotionPriority.IDLE.value, audio)
        self.popText.fadeOut()
        self.popText.unlock()
        self.popText.pop(msg)
        timer = QTimer(self.popText.currentTip)
        timer.timeout.connect(self.popText.fadeOut)
        timer.start(500 * len(msg))


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

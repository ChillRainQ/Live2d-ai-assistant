import io
import os
from abc import ABC, abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtGui import QImage

import live2d.v3 as live2d
from config.application_config import ApplicationConfig
from core.audio_generator import AudioGenerator
from live2d.v3.params import StandardParams
from ui.views.l2d_scene import Live2DScene
from utils import file_util
from utils.gobal_components import wav_handler


class Live2DModel(Live2DScene.CallbackSet):
    class CallbackSet(ABC):
        @abstractmethod
        def onPlayText(self, group: str, no: int):
            pass

        @abstractmethod
        def onPlaySound(self, group, no, audio_wav: io.BytesIO | AudioGenerator):
            pass

        @abstractmethod
        def onMotionSoundFinished(self):
            pass

        @abstractmethod
        def isSoundFinished(self) -> bool:
            pass

        @abstractmethod
        def onChatOpen(self):
            pass

    """
    Live2D 模型
    """

    def isFinished(self):
        return self.motionFinished and self.soundFinished

    def onLeftClick(self, mouseX, mouseY):
        pass

    def onInitialize(self):
        """
        初始化
        """
        self.initialize = True
        self.load_model()
        self.model_texture = QImage(file_util.get_live2d_texture_path(os.path.join(
            self.config.resource_dir.value, self.config.live2d_name.value,
            self.config.live2d_name.value + '.model3.json'
        )))
        # 初始化设置
        self.model.SetAutoBreathEnable(self.config.autoBreath.value)
        self.model.SetAutoBlinkEnable(self.config.autoBlink.value)

    def onResize(self, width, height):
        self.model.Resize(width, height)

    def onUpdate(self, width, height):
        """
        刷新动作
        """
        self.model.SetScale(self.config.scale.value)
        self.model.SetOffset(self.config.drawX.value, self.config.drawY.value)
        live2d.clearBuffer()
        self.model.Update()
        if wav_handler.Update():
            self.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                         wav_handler.GetRms() * self.config.lip_sync.value, 1)
        self.model.Draw()

    def onRightClick(self, mouseX, mouseY):
        self.callbackSet.onChatOpen()

    def onMouseMove(self, x: int, y: int):
        """
        鼠标移动
        """
        self.model.Drag(x, y)

    def onIntervalReached(self):
        self.startRandomMotion(live2d.MotionGroup.IDLE.value, live2d.MotionPriority.IDLE.value)

    initialize: bool  # 初始化标记
    model: live2d.LAppModel | None  # l2d模型
    motionFinished: bool  # 动作完成标记
    config: ApplicationConfig  # 配置
    model_texture: QImage | None  # 材质
    chatMotionSignal = Signal(str)

    def __init__(self):
        super().__init__()
        self.soundFinished = True
        self.initialize = False
        self.model = None
        self.motionFinished = True

    def load_model(self):
        """
        加载模型
        """
        if not self.initialize:
            return
        # 如果加载过模型，则重新加载
        if self.model is not None:
            del self.model
        self.model = live2d.LAppModel()
        self.model.LoadModelJson(os.path.join(
            self.config.resource_dir.value, self.config.live2d_name.value,
            self.config.live2d_name.value + '.model3.json'
        ))
        self.motionFinished = True

    def setup(self, config, callbackSet: CallbackSet):
        self.config = config
        self.callbackSet = callbackSet
        self.signalConnectSlot()

    def signalConnectSlot(self):
        self.config.autoBreath.valueChanged.connect(lambda value: self.model.SetAutoBreathEnable(value))
        self.config.autoBlink.valueChanged.connect(lambda value: self.model.SetAutoBreathEnable(value))

    def startMontion(self, group, no, priority):
        self.model.StartMotion(group, no, priority)

    def startOnMotionHandler(self, group, no, audio_wav: io.BytesIO = None | AudioGenerator):
        self.motionFinished = False
        self.callbackSet.onPlaySound(live2d.MotionGroup.IDLE.value, live2d.MotionPriority.IDLE.value, audio_wav)
        self.callbackSet.onPlayText(group, no)

    def startRandomMotion(self, group, no):
        self.model.StartRandomMotion(group, no,
                                     self.startOnMotionHandler,
                                     self.setMotionFinished)

    def startChatMotion(self, group, no, audio_wav: io.BytesIO = None | AudioGenerator):
        self.startOnMotionHandler(group, no, audio_wav)
        self.setMotionFinished()

    def setMotionFinished(self):
        self.motionFinished = True
        print("motion finished")

import os
from abc import ABC, abstractmethod

from PySide6.QtGui import QCursor, QImage
from live2d.v3.params import StandardParams

from config.application_config import ApplicationConfig
from l2d.LocalWavHandler import LocalWavHandler
from ui.views.l2d_scene import Live2DScene
import live2d.v3 as live2d

from utils import file_util

globalWavHandler = LocalWavHandler()


class Live2DModel(Live2DScene.CallbackSet):
    class CallbackSet(ABC):
        @abstractmethod
        def onPlayText(self, group: str, no: int):
            pass

        @abstractmethod
        def onPlaySound(self, group: str, no: int):
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
    initizlize: bool  # 初始化标记
    model: live2d.LAppModel | None  # l2d模型
    motionFinished: bool  # 动作完成标记
    config: ApplicationConfig  # 配置
    model_texture: QImage | None

    # callbackSet
    def __init__(self):
        super().__init__()
        self.initialize = False
        self.model = None
        self.motionFinished = True

    def onInitialize(self):
        """
        初始化
        """
        self.initialize = True
        self.load_model()
        self.model_texture = QImage(file_util.get_live2d_texture_path(os.path.join(
            self.config.live2d_resource_dir.value, self.config.live2d_name.value,
            self.config.live2d_name.value + '.model3.json'
        )))
        # 初始化设置
        self.model.SetAutoBreathEnable(self.config.autoBreath.value)
        self.model.SetAutoBlinkEnable(self.config.autoBlink.value)
        self.signalConnectSlot()

    def onResize(self, width, height):
        self.model.Resize(width, height)

    def onUpdate(self, width, height):

        self.model.SetScale(self.config.scale.value)
        self.model.SetOffset(self.config.drawX.value, self.config.drawY.value)

        live2d.clearBuffer()
        self.model.Update()
        if globalWavHandler.Update():
            self.model.SetParameterValue(StandardParams.ParamMouthOpenY,
                                         globalWavHandler.GetRms() * self.config.lip_sync.value, 1)
        self.model.Draw()

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
            self.config.live2d_resource_dir.value, self.config.live2d_name.value,
            self.config.live2d_name.value + '.model3.json'
        ))
        self.motionFinished = True

    def setup(self, config, callbackSet: CallbackSet):
        self.config = config
        self.callbacks = callbackSet

    def onMouseMove(self, x: int, y: int):
        """
        鼠标移动
        """
        self.model.Drag(x, y)

    def isInL2dArea(self, pos: QCursor.pos()):
        if self.model_texture is not None:
            pixel = self.model_texture.pixelColor(pos.x(), pos.y())
            if pixel.alpha() > 50:
                return True
        return False

    def signalConnectSlot(self):
        self.config.autoBreath.valueChanged.connect(lambda value: self.model.SetAutoBreathEnable(value))
        self.config.autoBlink.valueChanged.connect(lambda value: self.model.SetAutoBreathEnable(value))

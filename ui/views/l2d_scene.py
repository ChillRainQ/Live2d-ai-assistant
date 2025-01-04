from abc import ABC, abstractmethod

import OpenGL.GL as gl
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget

import core.send_event_back_application_win
import live2d.v3 as live2d
from config.application_config import ApplicationConfig
from core.gobal_components import i18n


class Live2DScene(QOpenGLWidget):
    class CallbackSet(ABC):
        @abstractmethod
        def onInitialize(self):
            pass

        @abstractmethod
        def onResize(self, width, height):
            pass

        @abstractmethod
        def onUpdate(self, width, height):
            pass

        @abstractmethod
        def onMouseMove(self, mouseX, mouseY):
            pass

        @abstractmethod
        def onRightClick(self, mouseX, mouseY):
            pass

        @abstractmethod
        def onLeftClick(self, mouseX, mouseY):
            pass

        @abstractmethod
        def onIntervalReached(self):
            pass

        @abstractmethod
        def isFinished(self):
            pass

    """
    l2d scene live2d 窗口
    """
    # 回调集合
    callbackSet: CallbackSet
    # 配置
    config: ApplicationConfig
    # 计时器
    timer: int
    # 间隔x
    jiffies: int

    def __init__(self):
        super().__init__()
        self.config = None
        self.lastX = -1
        self.lastY = -1
        self.timer = -1
        self.isMoving = False
        self.windowScale = self.devicePixelRatio()

    def setup(self, config: ApplicationConfig, callbackSet: CallbackSet):
        """
        设置窗口
        """
        self.config = config
        self.callbackSet = callbackSet
        self.setupAttributes()
        # 设置窗口大小
        self.resize(self.config.width.value, self.config.height.value)
        # 设置位置
        # screen = QApplication.primaryScreen()
        # geometry = screen.geometry()
        # self.move(geometry.width() - self.width(), geometry.height() - self.height())
        self.move(self.config.lastX.value, self.config.lastY.value)
        # 绑定信号槽
        self.signalConnectSlot()

    def setupAttributes(self):
        self.setWindowFlags(
            # 设置为工具类型窗口
            Qt.WindowType.Tool |
            # 无边框窗口
            Qt.WindowType.FramelessWindowHint

        )
        # 设置为透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 设置穿透
        # l2d_scene.setupAttributes.clickPenetrate.value
        print(f'{i18n.get_str("ui.views.l2d_scene.setupAttributes.clickPenetrate.value")}{self.config.clickPenetrate.value}')
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, self.config.clickPenetrate.value)
        self.setWindowTitle("live 2d scene")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.config.stay_on_top.value)
        self.show()

    def show(self):
        """
        展示l2d
        """
        # self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.config.stay_on_top.value)
        self.setVisible(self.config.visible.value)

    def initializeGL(self):
        """
        初始化OpenGL
        """
        self.makeCurrent()
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        live2d.glewInit()
        live2d.setGLProperties()
        self.callbackSet.onInitialize()

    def resizeGL(self, width: int, height: int):
        """
        重设宽高
        """
        self.callbackSet.onResize(width, height)

    def paintGL(self):
        """
        重绘
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        self.callbackSet.onUpdate(self.width(), self.height())

    def timerEvent(self, event):
        """
        定时器触发事件
        """
        # 窗口不可见，不用渲染
        if not self.isVisible():
            return

        if self.config.eye_track.value:
            """
            设定眼动跟踪
            """
            pos = QCursor.pos()
            self.callbackSet.onMouseMove(pos.x() - self.x(), pos.y() - self.y())

        if self.callbackSet.isFinished(): #动作结束
            """
            发生动作
            """
            self.jiffies -= 1 # 减少一帧
            if self.jiffies <= 0: # 渲染帧数耗尽， 进行下一个动作
                self.jiffies = self.config.fps.value * self.config.motion_interval.value
                self.callbackSet.onIntervalReached()
        self.update()

    def mousePressEvent(self, event):
        """
        鼠标按下事件
        """
        if not self.isIgnoreArea(event):
            core.send_event_back_application_win.click_back_app(event.globalX(),
                                                                event.globalY(),
                                                                event.button())
        else:
            self.lastX = event.x()
            self.lastY = event.y()
            self.isMoving = False

    def mouseReleaseEvent(self, event):
        """
        鼠标释放事件
        """
        if not self.isIgnoreArea(event):
            core.send_event_back_application_win.click_back_app(event.globalX(),
                                                                event.globalY(),
                                                                event.button())
        elif self.isMoving:
            pass
        elif event.button() == Qt.MouseButton.LeftButton:
            self.callbackSet.onLeftClick(event.x(), event.y())
        elif event.button() == Qt.MouseButton.RightButton:
            self.callbackSet.onRightClick(event.x(), event.y())
        self.isMoving = False

    def mouseMoveEvent(self, event):
        """
        鼠标拖拽事件
        """
        if self.isIgnoreArea(event) and (event.buttons() & Qt.MouseButton.LeftButton):
            # 计算并移动窗口位置
            self.move(event.globalX() - self.lastX, event.globalY() - self.lastY)
            self.config.lastX.value = self.x()
            self.config.lastY.value = self.y()
            self.isMoving = True

    def isIgnoreArea(self, event: QMouseEvent):
        height = self.height()
        x, y = event.pos().x(), event.pos().y()
        alpha = gl.glReadPixels(x * self.windowScale, (height - y) * self.windowScale, 1, 1, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)[3]
        return alpha > 0



    def signalConnectSlot(self):
        """
        信号槽绑定
        """
        self.config.fps.valueChanged.connect(self.setFps)
        self.config.visible.valueChanged.connect(self.setVisible)
        self.config.height.valueChanged.connect(self.setHeight)
        self.config.width.valueChanged.connect(self.setWidth)
        self.config.stay_on_top.valueChanged.connect(self.setOnTop)
        self.config.clickPenetrate.valueChanged.connect(self.setClickPenetrate)
        self.config.eye_track.valueChanged.connect(self.setEyeTrack)

    def setEyeTrack(self, value):
        self.config.eye_track.value = value

    def setFps(self, fps: int):
        self.jiffies = self.config.motion_interval.value * fps
        if self.timer != -1:
            self.killTimer(self.timer)
        self.timer = self.startTimer(1000 // fps)

    def setWidth(self, width: int):
        self.resize(width, self.height())

    def setHeight(self, height: int):
        self.resize(height, self.width())

    def setOnTop(self, onTop: bool):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, onTop)

    def setClickPenetrate(self):
        self.setupAttributes()
        self.raise_()

    def start(self):
        self.show()
        self.setFps(self.config.fps.value)



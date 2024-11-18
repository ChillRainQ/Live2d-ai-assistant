from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QWidget
from qfluentwidgets import  FlyoutViewBase, LineEdit, PrimaryToolButton, FluentIcon, ToolButton

from config.application_config import ApplicationConfig


class ChatBoxView(FlyoutViewBase):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout(self)
        self.lineEdit = LineEdit()
        self.lineEdit.setFixedWidth(200)
        self.sendMessageButton = PrimaryToolButton()
        self.sendMessageButton.setIcon(FluentIcon.SEND)
        self.closeButton = ToolButton()
        self.closeButton.setIcon(FluentIcon.CLOSE)
        hbox.addWidget(self.lineEdit)
        hbox.addWidget(self.sendMessageButton)
        hbox.addWidget(self.closeButton)


class FlyoutChatBox(QWidget):
    config: ApplicationConfig
    view: ChatBoxView
    sendMessageSignal = Signal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.view = ChatBoxView()
        self.hLayout = QHBoxLayout(self)

    def getSignalSlotMaps(self) -> dict:
        signal_slot_mapping = {
            self.view.closeButton.released: self.hide,
            self.view.sendMessageButton.released: self.__sendSignalAction,
            self.view.lineEdit.returnPressed: self.__sendSignalAction,
        }
        return signal_slot_mapping


    def setup(self, config: ApplicationConfig):
        self.config = config
        self.hLayout.addWidget(self.view)
        self.setAttributes()
        self.signalConnectSlot()

    def setAttributes(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Popup  # 弹出窗口
            | Qt.WindowType.FramelessWindowHint  # 无边框
            | Qt.WindowType.NoDropShadowWindowHint  # 禁用窗口阴影
        )

    def show(self):
        self.setVisible(True)
        self.move(self.config.lastX.value + self.config.width.value // 2 - self.width() // 2,
                  self.config.lastY.value + self.config.height.value + 10)
        self.activateWindow()

    def signalConnectSlot(self):
        for signal, slot in self.getSignalSlotMaps().items():
            signal.connect(slot)

    def __sendSignalAction(self):
        print("发送自定义信号：sendSignalAction")
        if len(self.view.lineEdit.text()) > 0:
            self.sendMessageSignal.emit(self.view.lineEdit.text())
        self.view.lineEdit.clear()

    def disable(self):
        self.view.sendMessageButton.setEnabled(False)

    def enable(self):
        self.view.sendMessageButton.setEnabled(True)





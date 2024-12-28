from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCursor
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QSystemTrayIcon, QApplication
from qfluentwidgets import CheckableMenu, FluentWindow


class SysTrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.action_ls = [
            QAction("打开设置")
        ]
        menu = CheckableMenu()
        menu.addSeparator()
        menu.addAction(self.action_ls)
        self.setContextMenu(menu)
        self.activated.connect(self.activatedAction)

    def activatedAction(self, reason):
        """
        托盘动作
        """
        if reason == self.ActivationReason.Context:
            self.contextMenu().show()
            self.contextMenu().move(QCursor.pos().x(), QCursor.pos().y() - self.contextMenu().height())

class GLPage(QOpenGLWidget):
    def __init__(self):
        super().__init__()

class Setting(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置")
        self.setWindowIcon()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)

    def show(self):
        self.hide()
        size = QApplication.primaryScreen().size()
        self.move(size.width() // 2 - self.width() // 2, size.height() // 2 - self.height() // 2)
        self.setVisible(True)
        self.adjustSize()
        self.setMicaEffectEnabled(True)



class App:
    def __init__(self):
        self.app = QApplication([])
        self.tray = SysTrayIcon()
        self.gl = GLPage()
        self.setting = Setting()

    def show(self):
        self.tray.show()
        self.gl.show()


if __name__ == "__main__":
    app = App()
    app.show()
    app.app.exec()
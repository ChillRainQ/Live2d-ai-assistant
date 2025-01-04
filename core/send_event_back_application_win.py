import win32api
import win32con
import win32gui
from PySide6.QtCore import Qt


def get_window_under_cursor(x, y):
    # 获取鼠标点击位置下方的最上层窗口句柄
    hwnd_top = win32gui.WindowFromPoint((x, y))
    return hwnd_top


def enum_windows_callback(hwnd, windows, x, y):
    # 获取窗口的矩形边界
    rect = win32gui.GetWindowRect(hwnd)
    win_x, win_y, width, height = rect

    # 判断鼠标位置是否在窗口内
    if win_x <= x <= win_x + width and win_y <= y <= win_y + height:
        windows.append(hwnd)


def get_second_window_under_cursor(x, y):
    # 存储所有窗口句柄
    windows = []

    # 枚举所有窗口
    win32gui.EnumWindows(enum_windows_callback, (windows, x, y))

    if len(windows) > 1:
        # 返回第二层窗口句柄，`windows[1]` 是第二个找到的窗口
        return windows[1]  # 第二层窗口

    return None

def click_back_app(x, y, click_type):
    pass
    x, y = win32api.GetCursorPos()
    hwnd = get_window_under_cursor(x, y)
    if click_type == Qt.MouseButton.LeftButton:
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, (y << 16) | x)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, (y << 16) | x)
    elif click_type == Qt.MouseButton.RightButton:
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, (y << 16) | x)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, (y << 16) | x)

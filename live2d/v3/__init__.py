from enum import Enum

from .live2d import *


class MotionPriority(Enum):
    NONE = 0
    IDLE = 1
    NORMAL = 2
    FORCE = 3


class MotionGroup(Enum):
    IDLE = "Idle"
    TAP_HEAD = "TapHead"


class HitArea(Enum):
    HEAD = MotionGroup.TAP_HEAD.value


LIVE2D_VERSION = 3

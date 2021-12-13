#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2

from core.snipper import ISnipper
# from .snipper import *
from .screenshot import ScreenShotWidget

class ScreenShotSnipper(ISnipper, ScreenShotWidget):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)

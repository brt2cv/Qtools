#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2

from core.snipper import ISnipper
from .screenshot import ScreenShotWidget

def make_snipper(win):
    return ScreenShotSnipper(win)

class ScreenShotSnipper(ISnipper, ScreenShotWidget):
    def run(self):
        self.take_snapshot()

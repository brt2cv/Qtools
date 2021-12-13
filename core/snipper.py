#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Link    : https://github.com/ianzhao05/textshot
# @Version : 0.0.1

class ISnipper:
    def __init__(self, win):
        self._win = win

    def __del__(self):
        """ QWindow关闭前，插件管理器释放插件对象 """
        pass

    def get_tray(self):
        """ 获取SystemTrayIcon图元对象 """
        return self._win.tray

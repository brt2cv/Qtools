#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Link    : https://github.com/ianzhao05/textshot
# @Version : 0.0.1

from traceback import print_exc

try:
    from utils.log import getLogger
    print("[+] {}: 启动调试Logger".format(__file__))
    logger = getLogger(0)
except ImportError:
    from logging import getLogger
    print("[!] {}: 调用系统logging模块".format(__file__))
    logger = getLogger(__file__)

class ISnipper:
    def __init__(self, win, *args, **kwargs):
        self._win = win
        super().__init__(*args, **kwargs)

    def __del__(self):
        """ QWindow关闭前，插件管理器释放插件对象 """

    def get_tray(self):
        """ 获取SystemTrayIcon图元对象 """
        return self._win.tray

    def _run(self):
        """ 框架调用的功能函数，调用run() """
        try:
            self.run()
        except Exception as e:
            logger.error(f"[!] 功能调用失败: {e}")
            print_exc()

    def run(self):
        """ 重写该方法，实现插件功能 """

def make_snipper(win):
    """ 生成snipper实例 """
    return ISnipper(win)

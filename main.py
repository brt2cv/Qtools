#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Link    : https://github.com/ianzhao05/textshot
# @Version : 0.4.1

import platform
from subprocess import call as subp_call

try:
    from system_hotkey import SystemHotkey
except Exception as e:
    print(f"[!] 未能加载模块【SystemHotkey】，将无法启用系统快捷键: {e}")
    SystemHotkey = None

try:
    from utils.log import getLogger
    print("[+] {}: 启动调试Logger".format(__file__))
    logger = getLogger(0)
except ImportError:
    from logging import getLogger
    print("[!] {}: 调用系统logging模块".format(__file__))
    logger = getLogger(__file__)

# from pynotifier import Notification
# def notify(msg):
#     Notification(title="TextShot", description=msg).send()

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def notify(msg):
    cmd = 'zenity --info --timeout=3 --text "{}" '.format(msg)
    subp_call(cmd, shell=True)

#####################################################################
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon
from PyQt5.QtWidgets import QStyle
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtDBus import QDBusConnection

def register_dbus(dbus_obj, serv_name):
    """
        服务端注册dbus函数，配合pyqtSlot使用。
        客户端测试：dbus-send --session --dest=$serv_name --type=method_call --print-reply  / local.Snipper.take_snapshot
    """
    session_bus = QDBusConnection.sessionBus()

    if not session_bus.isConnected():
        raise Exception("Fail to create a dbus connection.")

    if not QDBusConnection.sessionBus().registerService(serv_name):
        raise Exception("Fail to register the dbus service.")

    QDBusConnection.sessionBus().registerObject('/', dbus_obj
            , QDBusConnection.ExportNonScriptableSlots)
            # , QDBusConnection.ExportAllSlots)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 关闭所有窗口,也不关闭应用程序
        QApplication.setQuitOnLastWindowClosed(False)

        # PATH_LOGO = "/home/brt/reset.png"
        # assert os.path.exists(PATH_LOGO), "不存在托盘图标"
        # icon = QtGui.QIcon(PATH_LOGO)

        # icon = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(1, 1, QtGui.QImage.Format_Mono)))
        if platform.system() == "Windows":
            # icon = QApplication.style().standardIcon(QStyle.SP_VistaShield)
            icon = QApplication.style().standardIcon(QStyle.SP_BrowserReload)
        else:
            # 系统默认图标: https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
            icon = QtGui.QIcon.fromTheme("camera-web")

        self.setIcon(icon)  # self.icon = self.MessageIcon()
        # self._activate()

    def _activate(self):
        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.on_icon_clicked)
        # 把鼠标点击弹出消息的信号和槽连接
        self.messageClicked.connect(lambda: self.make_msg("【测试】点击消息"))

    def on_icon_clicked(self, reason):
        """ 鼠标点击icon传递的信号会带有一个整形的值：
            1: 表示单击右键
            2: 双击
            3: 单击左键
            4: 用鼠标中键点击
        """
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.show()

    def make_msg(self, msg):
        icon = QSystemTrayIcon.Information  # QSystemTrayIcon.NoIcon
        self.showMessage("提示", msg, icon)


from importlib import import_module
import os.path
import json
from traceback import print_exc

class MainWindow(QWidget):
    sig_keyhot = pyqtSignal(str)

    def __init__(self):
        """ if no ocr-need, pass the None """
        super().__init__()

        self.init_snippers()
        self._setup_ui()
        self._activate()

    def init_snippers(self):
        path_curr = os.path.dirname(__file__)
        path_appconf = os.path.join(path_curr, ".app.conf")
        if not os.path.exists(path_appconf):
            app_conf = {}
            for entry in os.scandir(os.path.join(path_curr, "app")):
                if entry.is_dir():
                    app_conf[entry.name] = os.path.join("app", entry.name)
            with open(path_appconf, "w") as fp:
                json.dump(app_conf, fp, ensure_ascii=False, indent=2)
        else:
            with open(path_appconf, "r") as fp:
                app_conf = json.load(fp)

        self.dict_snipper = {}
        for name, path in app_conf.items():
            try:
                self.load_snipper(name, path)
            except Exception as e:
                logger.error(f"[!] 插件加载失败【{name}: {path}】: {e}")
                print_exc()

    def load_snipper(self, name, path_appdir):
        module = import_module(path_appdir.replace(os.path.sep, "."))
        self.dict_snipper[name] = module.make_snipper(self)

    def app_exit(self):
        for snipper in self.dict_snipper.values():
            del snipper
        self.deleteLater()  # 删除托盘图标，无此操作的话，程序退出后托盘图标不会自动清除
        # self.tray.setVisible(False)
        QApplication.quit()

    def hotkey_slot(self, event, hotkey, args):
        # print(">>>", event, hotkey, args)
        return self.sig_keyhot.emit(args[0][0])

    def _setup_ui(self):
        from PyQt5.QtWidgets import QAction, QMenu

        self.setWindowTitle("DesktopTools")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        menu = QMenu()
        # menu.addAction(QAction("test", self, triggered=lambda: self.tray.make_msg("你好吗")))
        for name, snipper in self.dict_snipper.items():
            menu.addAction(QAction(name, self, triggered=snipper._run))
            if SystemHotkey is not None:
                hotkey_test = SystemHotkey(consumer=self.hotkey_slot)
                _names = name.split(maxsplit=1)
                if(len(_names) > 1):
                    # func = lambda msg: self.sig_keyhot.emit(name)  # lambda延迟绑定，name
                    # func = partial(hotkey_slot, name=name)
                    str_hotkey = _names[1][1:-1].replace("ctrl", "control")  # system_hotkey库标准命名control,不支持简写
                    hotkey_test.register(str_hotkey.split("+"), name)
        menu.addAction(QAction("退出", self, triggered=self.app_exit))

        self.tray = TrayIcon(self)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def _activate(self):
        self.sig_keyhot.connect(lambda snipper_name: self.dict_snipper[snipper_name]._run())

#####################################################################

if __name__ == "__main__":
    import sys
    # 可以使Qt在高DPI下正常显示：AA_EnableHighDpiScaling
    # QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    app = QApplication([])
    win = MainWindow()
    if platform.system() == "Linux":
        register_dbus(win, "tophats.desktool")
    sys.exit(app.exec_())

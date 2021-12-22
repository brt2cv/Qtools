#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2

# 参考: https://blog.csdn.net/weixin_47440418/article/details/108837426

from PyQt5.QtWidgets import QInputDialog, QMessageBox

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class ScreenShotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)  # 鼠标追踪
        self.setCursor(Qt.CrossCursor)  # 设置光标
        self.setWindowFlag(Qt.FramelessWindowHint)  # 窗口无边框
        self.setWindowState(Qt.WindowFullScreen)  # 窗口全屏

        self.snapshot = None
        self.painter = QtGui.QPainter()

    def take_snapshot(self):
        screen = QApplication.screenAt(QtGui.QCursor.pos())  # QGuiApplication.primaryScreen()
        win_id = QApplication.desktop().winId()  # 0
        self.snapshot = screen.grabWindow(win_id)

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.snapshot))
        self.setPalette(palette)
        self.update()

        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.start, self.end = None, None  # QtCore.QPoint() == QtCore.QPoint(0,0)
        self.show()

    def keyPressEvent(self, event):
        if self.snapshot and event.key() == Qt.Key_Escape:
            self.snapshot = None
        return super().keyPressEvent(event)

    # def _paint_background(self):
    #     shadowColor = QtGui.QColor(0, 0, 0, 100)  # 黑色半透明
    #     self.painter.drawPixmap(0, 0, self.snapshot)
    #     self.painter.fillRect(self.snapshot.rect(), shadowColor)     # 填充矩形阴影

    def paintEvent(self, event):
        if self.snapshot is not None:
            p = self.painter
            p.begin(self)  # 开始重绘

            # 绘制背景黑色半透明
            p.setPen(Qt.NoPen)
            p.setBrush(QtGui.QColor(0, 0, 0, 100))
            p.drawRect(0, 0, self.width(), self.height())

            # 绘制选取框
            if self.start != self.end:
                p.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 1, Qt.SolidLine, Qt.RoundCap))  # 设置画笔,蓝色,1px大小,实线,圆形笔帽
                p.setBrush(p.background())
                p.drawRect(QtCore.QRect(self.start, self.end))

            p.end()
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.snapshot = None
            self.close()  # 右键关闭当前绘图窗口
        elif self.snapshot is not None:
            self.start = self.end = event.pos()
            # if self.start.isNull():  # 错误
            self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.snapshot and self.start is not None:
            self.end = event.pos()
            self.update()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.snapshot is not None:
            if self.start == self.end:
                self.snapshot = None
                self.close()
                return super().mouseReleaseEvent(event)

            self.hide()
            QApplication.processEvents()  # 耗时任务防止假死
            im_pixmap = self.snapshot.copy(QtCore.QRect(self.start, self.end))
            self.processing(im_pixmap)
            self.snapshot = None
            self.close()
        return super().mouseReleaseEvent(event)

    def processing(self, im_pixmap):
        im_pixmap.save('picture.jpg', "jpg", quality=95)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    windows = ScreenShotWidget()
    windows.take_snapshot()
    sys.exit(app.exec_())

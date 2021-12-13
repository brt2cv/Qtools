from core.snipper import ISnipper
from PyQt5.QtWidgets import QInputDialog, QMessageBox

from .qrcode import QrcodeGenerator

class QrcodeSnipper(ISnipper, QrcodeGenerator):
    def run(self):
        msg, ok = QInputDialog.getMultiLineText(self._win, 'QRcode Generator', '输入内容', 'https://')
        if not ok and not msg:
            self.get_tray().make_msg("未检测到输入文本")
            return

        pil_img = self.make_qrcode(msg)
        qt_pixmap = pil_img.toqpixmap()

        msgbox = QMessageBox(QMessageBox.NoIcon, "Qrcode", "", parent=self._win)
        # msgbox.setStandardButtons(QMessageBox.NoButton)
        # msgbox.setDetailedText('版权：Bright Li\nTel: 18131218231\nE-mail: brt2@qq.com')
        msgbox.setIconPixmap(qt_pixmap)
        # msgbox.move(50,50)
        msgbox.show()  # exec_()

def make_snipper(win):
    return QrcodeSnipper(win)

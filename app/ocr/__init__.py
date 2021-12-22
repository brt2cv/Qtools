from core.snipper import ISnipper

import os.path
import numpy as np
from PIL import Image
import pyperclip

from .paddleocr import OCR_Engine
from app.screenshot.screenshot import ScreenShotWidget

def pixmap2ndarray(pixmap):
    img = Image.fromqpixmap(pixmap)
    return np.asarray(img)

class PaddleOcrSnipper(ISnipper, ScreenShotWidget):
    def __init__(self, *args_, **kwargs):
        super().__init__(*args_, **kwargs)
        self.ocr_engine = OCR_Engine()

    def run(self):
        self.take_snapshot()

    def processing(self, im_pixmap):
        im = pixmap2ndarray(im_pixmap)
        list_lines = self.ocr_engine.img2text(im)
        text = "\n".join(list_lines)
        pyperclip.copy(text)
        self.get_tray().make_msg(text)

def make_snipper(win):
    return PaddleOcrSnipper(win)

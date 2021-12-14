from core.snipper import ISnipper

import os.path
import numpy as np
from PIL import Image
import pyperclip

from .tools.infer.predict_system import TextSystem
from .tools.infer.utility import parse_args
from app.screenshot.screenshot import ScreenShotWidget

def pixmap2ndarray(pixmap):
    img = Image.fromqpixmap(pixmap)
    return np.asarray(img)

dir_curr = os.path.dirname(__file__)

def rpath(rpath):
    return os.path.join(dir_curr, rpath)

class PaddleOcrSnipper(ISnipper, ScreenShotWidget):
    def __init__(self, *args_, **kwargs):
        super().__init__(*args_, **kwargs)
        self.init_ocr_engine()

    def init_ocr_engine(self):
        args = parse_args()
        args.use_gpu = False
        args.cls_model_dir = rpath("models/ch_PP-OCRv2/ch_ppocr_mobile_v2.0_cls_infer")
        args.det_model_dir = rpath("models/ch_PP-OCRv2/ch_PP-OCRv2_det_infer")
        args.rec_model_dir = rpath("models/ch_PP-OCRv2/ch_PP-OCRv2_rec_infer")
        args.rec_char_dict_path = rpath("ppocr/utils/ppocr_keys_v1.txt")
        self.ocr_engine = TextSystem(args)

    def run(self):
        self.take_snapshot()

    def processing(self, im_pixmap):
        im = pixmap2ndarray(im_pixmap)

        list_lines = []
        result = self.ocr_engine(im)  # det & rec
        if result is not None:
            dt_box, tuple_rec = result
            for text, score in tuple_rec:
                print(f"[{score:.2f}] {text}")
                list_lines.append(text)
        text_lines = "\n".join(list_lines)

        pyperclip.copy(text_lines)
        self.get_tray().make_msg(text_lines)

def make_snipper(win):
    return PaddleOcrSnipper(win)

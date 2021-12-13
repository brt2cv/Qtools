from core.snipper import ISnipper

import os.path
import numpy as np
from PIL import Image
import pyperclip

from .paddleocr import TextSystem, parse_args
from app.screenshot.screenshot import ScreenShotWidget

def pixmap2ndarray(pixmap):
    img = Image.fromqpixmap(pixmap)
    return np.asarray(img)

class PaddleOcrSnipper(ISnipper, ScreenShotWidget, TextSystem):
    def __init__(self, *args, **kwargs):
        self.super(self, ISnipper).__init__(*args, **kwargs)

        args = parse_args()
        args.use_gpu = False

        dir_curr = os.path.dirname(__file__)
        args.cls_model_dir = os.path.join(dir_curr, "models/ch_PP-OCRv2/ch_ppocr_mobile_v2.0_cls_infer")
        args.det_model_dir = os.path.join(dir_curr, "models/ch_PP-OCRv2/ch_PP-OCRv2_det_infer")
        args.rec_model_dir = os.path.join(dir_curr, "models/ch_PP-OCRv2/ch_PP-OCRv2_rec_infer")
        self.super(self, TextSystem).__init__(args)

    # def file2text(self, path_img):
    #     im = cv2.imread(path_img)
    #     return self.img2text(im)

    def img2text(self, im):
        text_lines = []
        result = self.__call__(im)  # det & rec
        if result is not None:
            dt_box, tuple_rec = result
            for text, score in tuple_rec:
                print(f"[{score:.2f}] {text}")
                text_lines.append(text)
        return "\n".join(text_lines)

    def run(self):
        self.take_snapshot()

    def processing(self, im_pixmap):
        im = pixmap2ndarray(im_pixmap)
        text_lines = self.img2text(im)

        pyperclip.copy(text_lines)
        self.get_tray().make_msg(text_lines)


def make_snipper(win):
    return PaddleOcrSnipper(win)

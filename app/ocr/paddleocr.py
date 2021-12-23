#!/usr/bin/env python3
# @Date    : 2021-12-22
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2

# 参考: https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/paddleocr.py
# 模型下载: https://github.com/brt2cv/kaggle/releases/download/PP-OCRv2.1/models.7z

import os.path

if __name__ == "__main__":
    from tools.infer.predict_system import TextSystem
    from tools.infer.utility import parse_args
else:
    from .tools.infer.predict_system import TextSystem
    from .tools.infer.utility import parse_args

dir_curr = os.path.dirname(__file__)
def rpath(rpath):
    return os.path.join(dir_curr, rpath)

class OCR_Engine:
    ocr_det_model_server = rpath("models/ch_PP-OCRv2/ch_ppocr_server_v2.0_det_infer")
    ocr_det_model_mobile = rpath("models/ch_PP-OCRv2/ch_PP-OCRv2_det_infer")
    ocr_rec_model_server = rpath("models/ch_PP-OCRv2/ch_ppocr_server_v2.0_rec_infer")
    ocr_rec_model_mobile = rpath("models/ch_PP-OCRv2/ch_PP-OCRv2_rec_infer")
    ocr_cls_model = rpath("models/ch_PP-OCRv2/ch_ppocr_mobile_v2.0_cls_infer")
    rec_char_dict = rpath("ppocr/utils/ppocr_keys_v1.txt")

    def __init__(self):
        # version 2.1
        args = parse_args()

        args.use_gpu = False
        args.det_model_dir = self.ocr_det_model_server
        if not os.path.exists(args.det_model_dir):
            args.det_model_dir = self.ocr_det_model_mobile
        args.rec_model_dir = self.ocr_rec_model_server
        if not os.path.exists(args.rec_model_dir):
            args.rec_model_dir = self.ocr_rec_model_mobile
        args.cls_model_dir = self.ocr_cls_model
        args.rec_char_dict_path = self.rec_char_dict

        self.engine = TextSystem(args)

    def img2text(self, im, print_score=False):
        """ return a list of strings of OCR """
        result = self.engine(im)  # det & rec
        if result is None:
            return []
        if print_score:
            dt_box, tuple_rec = result
            for text, score in tuple_rec:
                # print(text)
                print(f"[{score:.2f}] {text}")
        return [i[0] for i in result[1]]


if __name__ == "__main__":
    import cv2

    ocr = OCR_Engine()
    list_text = ocr.img2text(cv2.imread("tmp/test.jpg"))
    print(">>>", list_text)

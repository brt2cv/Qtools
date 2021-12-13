#!/usr/bin/env python3
# @Date    : 2021-12-13
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2

import qrcode

class QrcodeGenerator:
    def __init__(self):
        self.qrcode_generator = qrcode.QRCode(
            # 设置Version，范围1~40 即21*21 ~ 177*177
            version=2,
            # 纠错率，有L,M,Q,H四种，分别对应7%，15%，25%，30%，默认为ERROR_CORRECT_M
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            # 每个方块的像素个数
            box_size=6,
            # 二维码距图像外围边框的距离，默认为4
            border=2
        )

    def make_qrcode(self, msg):
        self.qrcode_generator.clear()
        self.qrcode_generator.add_data(msg)
        self.qrcode_generator.make(fit=True)
        pil_img = self.qrcode_generator.make_image(fill_color="black", back_color="white")
        return pil_img

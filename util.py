#!/usr/bin/env python3
# @Date    : 2021-12-23
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.1

import numpy as np
import cv2

def _bytes2im(bytes_img, size):
    # return np.asarray(bytearray(bytes_img), "uint8").reshape(size)
    return np.fromstring(bytes_img, "unit8").reshape(size)

def bytes2im(bytes_img):
    return cv2.imdecode(np.frombuffer(bytes_img, np.uint8), cv2.IMREAD_COLOR)

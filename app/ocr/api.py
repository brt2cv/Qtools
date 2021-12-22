#!/usr/bin/env python3
# @Date    : 2021-12-22
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.0

import io
from fastapi import APIRouter
from fastapi import File, UploadFile

router = APIRouter(prefix="/ocr")

#####################################################################
from .paddleocr import OCR_Engine
# from imageio import imread as imread_bytes
import cv2
import numpy as np

def imread_bytes(bytes_img):
    return cv2.imdecode(np.frombuffer(bytes_img, np.uint8), cv2.IMREAD_COLOR)

OCR = OCR_Engine()

@router.post("/")
async def img2text(image: UploadFile=File(...)):
    """ 识别上传图像中的字符（支持中文），并返回文字 """
    bytes_img = await image.read()
    # np.fromstring(bytes_img, "unit8").reshape()
    # imageio.imread(io.BytesIO(bytes_img))
    im = imread_bytes(bytes_img)
    return OCR.img2text(im)

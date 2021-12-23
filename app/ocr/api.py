#!/usr/bin/env python3
# @Date    : 2021-12-23
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.1

from fastapi import APIRouter
from fastapi import File, UploadFile

router = APIRouter(prefix="/ocr")

#####################################################################
from .paddleocr import OCR_Engine
import util
# from imageio import imread as imread_bytes

engine = None
def get_engine():
    global engine

    if engine is None:
        engine = OCR_Engine()
    return engine

@router.post("/")
async def img2text(image: UploadFile=File(...)):
    """ 识别上传图像中的字符（支持中文），并返回文字 """
    bytes_img = await image.read()
    # np.fromstring(bytes_img, "unit8").reshape()
    # imageio.imread(io.BytesIO(bytes_img))
    im = util.bytes_img(bytes_img)
    return get_engine().img2text(im)

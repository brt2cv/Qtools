#!/usr/bin/env python3
# @Date    : 2021-12-22
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.0

import os
from loguru import logger

from fastapi import APIRouter
from fastapi import File, UploadFile

import util
from .facenet import FaceRecognizer


dir_curr = os.path.dirname(__file__)
def rpath(rpath):
    return os.path.join(dir_curr, rpath)

# 存储地址
dir_face_db = rpath("face_db/")
if not os.path.exists(dir_face_db):
    os.mkdir(dir_face_db)

app = APIRouter(prefix="/face")
engine = None
def get_engine():
    global engine

    if engine is None:
        engine = FaceRecognizer()
    return engine

@app.post("/thresh")
async def reset_threshold(thresh: float):
    get_engine().reset_threshold(thresh)
    return "ok"

@app.post("/faceRec")
async def face_recognize(image: UploadFile=File(...)):
    """ 识别上传的人脸图像，返回可能的人员列表和可能性 """
    logger.debug(f"识别图像")
    bytes_img = await image.read()
    engine = get_engine()
    names, boxes = engine.recognize(util.bytes2im(bytes_img))
    logger.info(f"结果: names: {names}\nboxes: {boxes}")
    return names

@app.post("/register")
async def face_register(name: str, image: UploadFile=File(...)):
    logger.debug(f"接收到{name}的注册头像")
    _, ext = os.path.splitext(image.filename)
    path_save = os.path.join(dir_face_db, name+ext)
    if os.path.exists(path_save):
        return "err: 用户已注册"
    bytes_img = await image.read()
    save_face(bytes_img, path_save)
    return "ok"

@app.post("/register_update")
async def face_update(name: str, image: UploadFile=File(...)):
    _, ext = os.path.splitext(image.filename)
    path_save = os.path.join(dir_face_db, name+ext)
    bytes_img = await image.read()
    save_face(bytes_img, path_save)
    return "ok"

def save_face(bytes_img, path_save):
    with open(path_save, "wb") as fp:
        fp.write(bytes_img)

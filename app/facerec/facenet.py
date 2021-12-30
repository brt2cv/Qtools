#!/usr/bin/env python3
# @Date    : 2021-12-30
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.2

import numpy as np
import cv2
import paddle
from loguru import logger

import os, sys
dir_curr = os.path.dirname(__file__)

if dir_curr not in sys.path:  # os.environ["path"]:
    sys.path.append(dir_curr)
from MobileFaceNet.detection.face_detect import MTCNN

def rpath(rpath):
    return os.path.join(dir_curr, rpath)

def regularization(img):
    img = img.transpose((2, 0, 1))
    img = (img - 127.5) / 127.5
    return img

def feature_similar(feat, feat2):
    """ return the prob of two features """
    return np.dot(feat, feat2) / (np.linalg.norm(feat) * np.linalg.norm(feat2))

class FaceRecognizer:
    Threshold = 0.6
    dir_faces = rpath("face_db")
    path_det_model = rpath("MobileFaceNet/models/mtcnn")
    path_rec_model = rpath("MobileFaceNet/models/infer/model")

    def __init__(self):
        self.mtcnn = MTCNN(self.path_det_model)
        self.model = paddle.jit.load(self.path_rec_model)
        self.model.eval()
        self._load_registers()

    def _load_registers(self):
        self.faces_db = {}  # name: feature
        for entry in os.scandir(self.dir_faces):
            # im = cv2.imread(entry.path)  # cv2的Bug: 中文路径，返回None
            im = cv2.imdecode(np.fromfile(entry.path, dtype=np.uint8), -1)
            faces, _ = self.detect_faces(im)
            # assert len(faces) == 1, f"注册库中每张图片的人脸只能有一个，【{entry.path}】错误"
            feature = self._infer(faces[0])

            name, _ = os.path.splitext(entry.name)
            self.faces_db[name] = feature[0]

    def detect_faces(self, im):
        faces, boxes = self.mtcnn.infer_image(im)
        if faces is None:
            return [], []
        faces = list(map(regularization, faces))
        return faces, boxes

    def face_register(self, name, im_face):
        """ 注册人脸，并将之存储于人脸库目录 """
        path_save = os.path.join(self.dir_faces, name, ".jpg")
        # cv2.imwrite()
        cv2.imencode('.jpg', im_face)[1].tofile(path_save)

    def _infer(self, im_face):
        """ 识别图像，返回人脸特征 """
        dim = len(im_face.shape)
        assert dim in [3, 4], f"当前图片维度【{dim}】，不符合'dim=(3 or 4)'的要求"
        if dim == 3:
            im_face = im_face[np.newaxis, :]
        tensor_face = paddle.to_tensor(im_face, dtype='float32')
        # 执行预测
        feature = self.model(tensor_face)
        return feature.numpy()

    @classmethod
    def reset_threshold(cls, threshold):
        cls.Threshold = threshold

    def recognize(self, img):
        """ return (faces_name: list, boxes: list) """
        faces_name = []
        faces, boxes = self.detect_faces(img)
        if faces:
            faces = np.array(faces, dtype='float32')  # faces is a list, change to ndarray
            features = self._infer(faces)
            logger.debug(f">> 共计检索到【{len(features)}】张面孔")
            for i, curr_feat in enumerate(features):
                dict_prob = {}
                for name, db_feat in self.faces_db.items():
                    dict_prob[name] = feature_similar(curr_feat, db_feat)
                sort_prob = sorted(dict_prob.items(), key=lambda d: d[1], reverse=True)
                logger.debug(f'人脸【{i}】对比结果： {sort_prob}')
                # 处理结果
                name, prob = sort_prob[0]
                faces_name.append(name if prob > self.Threshold else "unknown")
        return faces_name, boxes

#####################################################################
from PIL import ImageDraw, ImageFont, Image

def add_text(img, text, left, top, color=(0, 0, 0), size=20):
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(rpath('MobileFaceNet/simfang.ttf'), size)
    draw.text((left, top), text, color, font=font)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def draw_faces(img, names, boxes):
    """ 画出人脸框和关键点 """
    for i, name in enumerate(names):
        bbox = boxes[i, :4]
        corpbbox = [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
        cv2.rectangle(img, (corpbbox[0], corpbbox[1]), (corpbbox[2], corpbbox[3]), (255, 0, 0), 1)
        img = add_text(img, name, corpbbox[0], corpbbox[1] -15, color=(0, 0, 255), size=12)
    return img

def getopt():
    import argparse

    parser = argparse.ArgumentParser("MobileFaceNet", description="人脸识别程序")
    parser.add_argument("-c", "--camera_as_input", action="store_true", help="使用摄像头")
    return parser.parse_args()

# copy from: ipynb/OCR/opencv_ocr.py
kWinName = "EAST: An Efficient and Accurate Scene Text Detector"
def faces_recognize(img):
    names, boxes = predictor.recognize(img)
    logger.info(f"结果: names: {names}\nboxes: {boxes}")
    img = draw_faces(img, names, boxes)
    cv2.imshow(kWinName, img)


if __name__ == "__main__":
    args = getopt()

    predictor = FaceRecognizer()
    if args.camera_as_input:
        cv2.namedWindow(kWinName, cv2.WINDOW_NORMAL)

        cap = cv2.VideoCapture(0)
        while cv2.waitKey(1) < 0:
            # Read frame
            hasFrame, img = cap.read()
            if not hasFrame:
                cv2.waitKey()
                break
            faces_recognize(img)
    else:
        img = cv2.imread("MobileFaceNet/dataset/test.jpg")
        # img = cv2.imread("../ocr/tmp/test.jpg")
        faces_recognize(img)
        cv2.waitKey(0)

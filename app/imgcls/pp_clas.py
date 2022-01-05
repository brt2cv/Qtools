#!/usr/bin/env python3
# @Date    : 2022-01-05
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.0

# 制作数据集 ==>> 数据集切分 ==>> 训练:测试:验证=7:1:2
# paddlex --split_dataset --format ImageNet --dataset_dir './dataset/' --val_value 0.2 --test_value 0.1

import os, sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
__ppcls__ = os.path.join(__dir__, "PaddleClas")
if __ppcls__ not in sys.path:
    sys.path.append(__ppcls__)

from ppcls.utils import config
from ppcls.engine.engine import Engine

# from ppcls.utils.check import check_gpu
import paddle  # import is_compiled_with_cuda

def rpath(rpath):
    return os.path.join(__dir__, rpath)

class ImgClsEngine(Engine):
    def __init__(self, path_conf, mode="infer"):
        conf = config.get_config(args.config, show=False)
        conf["Global"]["device"] = "gpu" if paddle.is_compiled_with_cuda() else "cpu"

        super().__init__(conf, mode)
        if mode == "infer":
            self.model.eval()

    def train(self, dir_ds, path_lb):
        self.config["DataLoader"]["Train"]["dataset"]["image_root"] = dir_ds
        self.config["DataLoader"]["Train"]["dataset"]["cls_label_path"] = path_lb
        return super().train()

    @paddle.no_grad()
    def infer(self, bytes_imgs):
        """ 重写Engine.infer()这个丑陋的代码...整个class都及其丑陋！ """
        batch_size = self.config["Infer"]["batch_size"]

        results = []
        batch_data = []
        for idx, bImg in enumerate(bytes_imgs):
            for process in self.preprocess_func:
                x = process(bImg)
            batch_data.append(x)

            if len(batch_data) >= batch_size or idx == len(bytes_imgs) - 1:
                batch_tensor = paddle.to_tensor(batch_data)
                out = self.model(batch_tensor)
                if isinstance(out, list):
                    out = out[0]
                if isinstance(out, dict):
                    out = out["output"]
                result = self.postprocess_func(out, file_names=None)
                results.append(result)
                batch_data.clear()
        return results

def getopt():
    import argparse
    parser = argparse.ArgumentParser("ImageClassification", description="")
    parser.add_argument("config", action="store", help="config file path, pass 'DFT' for 'configs/config.yaml'")
    parser.add_argument("-t", "--train", action="store", help="执行训练，请输入datasets目录（labels=dir_ds/labels.txt）")
    parser.add_argument("-i", "--infer", action="store", help="图像预测，请输入需要检测的图片路径")
    parser.add_argument("-g", "--gpu", action="store_true", help="使用 CPU 或者 GPU ==>> deprated: 自动识别")
    return parser.parse_args()

if __name__ == "__main__":
    args = getopt()

    if args.gpu:
        print("[!] Warning: Paddle自动识别模块是否为GPU，请勿手动传参")
    # if args.config == "DFT":
    #     args.config = "configs/config.yaml"

    if args.train:
        dir_dataset = args.train
        path_labels = os.path.join(dir_dataset, "labels.txt")
        ImgClsEngine(args.config, mode="train").train(dir_dataset, path_labels)
        sys.exit()

    # infer
    eng = ImgClsEngine(args.config, mode="infer")
    path_img = args.infer if args.infer else "tmp/test.jpg"
    with open(path_img, "rb") as fp:
        bytes_img = fp.read()
    results = eng.infer(bytes_img)
    print(">>>", results)

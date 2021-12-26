#!/usr/bin/env python3
# @Date    : 2021-12-26
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.0.1

import tensorflow as tf
import tensorflow_hub as hub

# Load the input image.
image_path = 'tmp/dance.jpg'
image = tf.io.read_file(image_path)
image = tf.compat.v1.image.decode_jpeg(image)
image = tf.expand_dims(image, axis=0)
# Resize and pad the image to keep the aspect ratio and fit the expected size.
image = tf.cast(tf.image.resize_with_pad(image, 192, 192), dtype=tf.int32)
model = hub.load("https://hub.tensorflow.google.cn/google/movenet/singlepose/lightning/4")

# image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)
# model = hub.load("https://hub.tensorflow.google.cn/google/movenet/singlepose/thunder/4")

# image = tf.cast(tf.image.resize_with_pad(image, 256, 256), dtype=tf.int32)
# model = hub.load("https://hub.tensorflow.google.cn/google/movenet/multipose/lightning/1")

movenet = model.signatures['serving_default']

# Run model inference.
outputs = movenet(image)
keypoints = outputs['output_0']
print(keypoints)

# 鼻子
# 左眼和右眼
# 左耳和右耳
# 左肩和右肩
# 左肘和右肘
# 左腕和右腕
# 左臀和右臀
# 左膝和右膝
# 左脚踝和右脚踝

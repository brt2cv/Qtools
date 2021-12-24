#!/usr/bin/env python3
# @Date    : 2021-12-24
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.0

# reference: https://github.com/PaddlePaddle/models/tree/develop/PaddleCV/human_pose_estimation

import paddlehub as hub
module = hub.Module(name="human_pose_estimation_resnet50_mpii")

# set input dict
input_dict = {"image": ['path/to/image']}

# execute predict and print the result
results = module.keypoint_detection(data=input_dict)
for result in results:
    print(result['path'])
    print(result['data'])

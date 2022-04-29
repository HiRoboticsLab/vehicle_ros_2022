#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge
import numpy as np

from dynamic_reconfigure.server import Server
from vehicle_mission.cfg import laneConfig


config_kernel = 5
config_threshold_low = 220
config_threshold_high = 255

cv_bridge = CvBridge()


def callback(data):

    global config_kernel, config_threshold_low, config_threshold_high

    try:

        # 话题转图片
        image = cv_bridge.compressed_imgmsg_to_cv2(data)

        # # 处理黑白
        # gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # COLOR_BGR2GRAY

        # 处理形态梯度
        kernel = np.ones((config_kernel, config_kernel), np.uint8)
        gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
        # 灰度
        gray = cv2.cvtColor(gradient, cv2.COLOR_RGB2GRAY)
        # 背景图
        bg = np.copy(gray)
        bg[::] = 0
        # 图片非操作
        result = cv2.bitwise_not(gray, bg)

        ret, thresh = cv2.threshold(
            result, config_threshold_low, config_threshold_high, cv2.THRESH_BINARY)

        # 图片转话题
        gray_img_msg = cv_bridge.cv2_to_compressed_imgmsg(thresh)
        pub_lane.publish(gray_img_msg)

    except Exception as e:
        rospy.logerr('%s' % e)


def callback_param(config, level):
    global config_kernel, config_threshold_low, config_threshold_high

    rospy.loginfo("""Reconfiugre Request: {kernel}, {threshold_low}, {threshold_high}""".format(**config))

    config_kernel = config.kernel
    config_threshold_low = config.threshold_low
    config_threshold_high = config.threshold_high

    return config


if __name__ == '__main__':

    rospy.init_node('camera_detect_lane')

    # config_kernel = rospy.get_param('kernel', 10)
    # config_threshold_low = rospy.get_param('threshold_low', 200)
    # config_threshold_high = rospy.get_param('threshold_high', 255)

    rospy.Subscriber('/video_source/compress/compressed', CompressedImage, callback) \

    pub_lane = rospy.Publisher('/detect_lane', CompressedImage, queue_size=10) \

    # 参数服务
    Server(laneConfig, callback_param)

    rospy.spin()

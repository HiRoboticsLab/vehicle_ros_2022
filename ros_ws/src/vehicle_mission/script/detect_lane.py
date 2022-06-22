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

hl, sl, vl = 0, 0, 0
hh, sh, vh = 50, 60, 150

cv_bridge = CvBridge()


# 处理hsv
def detect_hsv(image):
    global hl, sl, vl, hh, sh, vh
    lower = np.array([hl, sl, vl])
    upper = np.array([hh, sh, vh])
    # gauss = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return mask


# 处理形态梯度
def detect_morph_gradient(image):
    global config_kernel, config_threshold_low, config_threshold_high
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

    return thresh

def calc_yaw_angle(image):
    image[0: int(image.shape[0] / 4 * 3)] = 0
    try:
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=cv2.contourArea, reverse=True)
        (x, y, w, h) = cv2.boundingRect(contours[0])
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2, cv2.LINE_AA)
        # 中点
        M = cv2.moments(contours[0])
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])

        cv2.circle(image, (center_x, center_y), 1, (0, 0, 255), -1)
        return image, center_x, center_y
    except Exception:
        pass


def callback(data):
    try:
        # 话题转图片
        image = cv_bridge.compressed_imgmsg_to_cv2(data)

        # # 处理黑白
        # gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # COLOR_BGR2GRAY

        result_morph = detect_morph_gradient(image)
        result_hsv = detect_hsv(image)

        result_morph = 255 - result_morph
        result = cv2.bitwise_and(result_morph, result_hsv)

        # 膨胀
        kernel = np.ones((5, 5), dtype=np.uint8)
        dilate = cv2.dilate(result, kernel, 1)
        # gauss = cv2.GaussianBlur(result, (25, 25), 0)
        result, x, y = calc_yaw_angle(dilate)

        # 图片转话题
        gray_img_msg = cv_bridge.cv2_to_compressed_imgmsg(result)
        pub_lane.publish(gray_img_msg)

    except Exception as e:
        rospy.logerr('%s' % e)


def callback_param(config, level):
    global config_kernel, config_threshold_low, config_threshold_high

    global hl, sl, vl, hh, sh, vh

    # rospy.loginfo("""Reconfiugre Request: {kernel}, {threshold_low}, {threshold_high}""".format(**config))

    config_kernel = config.kernel
    config_threshold_low = config.threshold_low
    config_threshold_high = config.threshold_high

    hl = config.hl
    sl = config.sl
    vl = config.vl
    hh = config.hh
    sh = config.sh
    vh = config.vh

    return config


if __name__ == '__main__':

    rospy.init_node('camera_detect_lane')

    rospy.Subscriber('/video_source/compress/compressed', CompressedImage, callback) \

    pub_lane = rospy.Publisher('/detect_lane', CompressedImage, queue_size=10) \

    # 参数服务
    Server(laneConfig, callback_param)

    rospy.spin()

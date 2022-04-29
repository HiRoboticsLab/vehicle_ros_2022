#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
import math


# class Wheel():

#     def __init__(self, callback):
#         self.listener_wheel = rospy.Subscriber('cmd_wheel', Int32MultiArray, self.on_receive_msg, 10) \

#         self.talker_wheel = rospy.Publisher('wheel', Int32MultiArray, queue_size=10)
#         self.sender = callback

#     def on_receive_msg(self, msg, args):
#         rospy.logdebug('receive cmd --> wheel : "%s"' % msg)
#         try:
#             data = msg.data
#             left = data[0]
#             right = data[1]
#             obj = {
#                 'to': 'wheel',
#                 'data': [left, right]
#             }
#             # stm32接收换行表示结尾
#             json_str = json.dumps(obj) + "\r\n"
#             self.sender(json_str)
#         except Exception as e:
#             rospy.logerr('%s' % e)

#     def report(self, array_wheel):
#         # rospy.logdebug('report wheel : "%s"' % array_wheel)
#         try:
#             msg_wheel = Int32MultiArray()
#             msg_wheel.data = array_wheel
#             self.talker_wheel.publish(msg_wheel)
#         except Exception as e:
#             rospy.logerr('%s' % e)


class Wheel():

    # 参数设定(米)
    wheel_distance = 0.18
    wheel_diameter = 0.065
    wheel_laps_code = 341.2

    tick2rad = (360 / (wheel_laps_code)) * math.pi / 180

    def __init__(self, callback):
        self.listener_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.on_receive_msg, queue_size=10) \

        self.talker_wheel = rospy.Publisher('wheel', Int32MultiArray, queue_size=10)
        self.sender = callback

    def on_receive_msg(self, msg):
        rospy.logdebug('receive cmd --> cmd_vel : "%s"' % msg)
        try:
            # 智能车内部100ms算一次pwm，所以除以10
            vehicle_speed = msg.linear.x / 10
            vehicle_angular = msg.angular.z / 10
            vehicle_angular = vehicle_angular * -1

            # 声明变量
            vehicle_speed_left, vehicle_speed_right = 0, 0

            # 计算速度
            vehicle_speed_left = ((2 * vehicle_speed) +
                                  (vehicle_angular * self.wheel_distance)) / 2
            vehicle_speed_right = 2 * vehicle_speed - vehicle_speed_left

            # 计算码盘期望值
            vehicle_code_left = vehicle_speed_left / \
                (self.wheel_diameter / 2) / self.tick2rad
            vehicle_code_right = vehicle_speed_right / \
                (self.wheel_diameter / 2) / self.tick2rad

            # 准备数据
            obj = {
                'to': 'wheel',
                'data': [vehicle_code_left, vehicle_code_right]
            }

            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            rospy.logerr('%s' % e)

    def report(self, array_wheel):
        # rospy.logdebug('report wheel : "%s"' % array_wheel)
        try:
            msg_wheel = Int32MultiArray()
            msg_wheel.data = array_wheel
            self.talker_wheel.publish(msg_wheel)
        except Exception as e:
            rospy.logerr('%s' % e)

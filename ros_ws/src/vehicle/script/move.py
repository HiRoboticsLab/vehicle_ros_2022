#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
机器人运动分析参考文献
https://mp.weixin.qq.com/s/Mj5iLR_4TKeJiaOVqJf6Vg
    因为
        Vc = WR
        Vleft = W(R - L/2)
        Vright = W(R + L/2)
    所以
        W = (Vright - Vleft) / L
        Vc = (Vleft + Vright) / 2
        Rc = L(Vl + Vr) / 2(Vr - Vl)
每秒脉冲数 = 一圈脉冲数 * 倍频数 /（车轮直径 * PI）* 速度
每米脉冲数 = 一圈脉冲数 * 倍频数 /（车轮直径 * PI）
速度 = 每秒脉冲数 / 每米脉冲数

pip install sympy
'''

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray
import math


class Move():

    # 参数设定(米)
    wheel_distance = 0.18
    wheel_diameter = 0.065
    wheel_laps_code = 224.5
    last_angle = 0
    # pose_x, pose_y, pose_angle = 0, 0, 0
    pose_x, pose_y = 0, 0
    # 每个脉冲对应的弧度
    tick2rad = (360 / (wheel_laps_code * 2)) * math.pi / 180

    def __init__(self):
        self.listener_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.on_receive_msg, queue_size=10) \

        self.publisher_wheel = rospy.Publisher('vehicle/cmd_wheel', Int32MultiArray, queue_size=10) \


    def on_receive_msg(self, msg):
        # rospy.logdebug('receive cmd --> light : "%s"' % msg)
        try:
            rospy.logdebug('receive cmd --> cmd_vel : "%s"' % msg)

            # 智能车内部50ms算一次pwm，所以除以20
            vehicle_speed = msg.linear.x / 10
            # vehicle_angular = msg.angular.z / 20
            vehicle_angular = msg.angular.z / 2
            vehicle_angular = vehicle_angular * -1

            # 声明变量
            vehicle_speed_left, vehicle_speed_right = 0, 0

            # vehicle_speed_left = sp.Symbol('vehicle_speed_left')
            # vehicle_speed_right = sp.Symbol('vehicle_speed_right')
            # # 声明计算公式
            # result = sp.solve(
            #     [
            #         (vehicle_speed_left + vehicle_speed_right) / 2 - vehicle_speed,                     \
            #         (vehicle_speed_right - vehicle_speed_left) / self.wheel_distance - vehicle_angular  \
            #     ],                                                                                      \
            #     [vehicle_speed_left, vehicle_speed_right]
            # )

            vehicle_speed_left = ((2 * vehicle_speed) +
                                  (vehicle_angular * self.wheel_distance)) / 2
            vehicle_speed_right = 2 * vehicle_speed - vehicle_speed_left

            vehicle_code_left = vehicle_speed_left / \
                (self.wheel_diameter / 2) / self.tick2rad
            vehicle_code_right = vehicle_speed_right / \
                (self.wheel_diameter / 2) / self.tick2rad


            # if(abs(vehicle_angular) > (0.6 / 20)):
            #     if vehicle_angular > 0:
            #         vehicle_code_left = 0
            #     if vehicle_angular < 0:
            #         vehicle_code_right = 0


            wheel_msg = Int32MultiArray()
            wheel_msg.data = [int(vehicle_code_left), int(vehicle_code_right)]

            self.publisher_wheel.publish(wheel_msg)

        except Exception as e:
            rospy.logerr('%s' % e)


# 主函数
if __name__ == '__main__':

    rospy.init_node('vehicle_move', anonymous=True)
    move = Move()

    rospy.spin()

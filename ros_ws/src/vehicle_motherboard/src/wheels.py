#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import Int32MultiArray


class Wheel():

    def __init__(self, callback):
        self.listener_wheel = rospy.Subscriber('cmd_wheel', Int32MultiArray, self.on_receive_msg, 10) \

        self.talker_wheel = rospy.Publisher('wheel', Int32MultiArray, queue_size=10)
        self.sender = callback

    def on_receive_msg(self, msg, args):
        rospy.logdebug('receive cmd --> wheel : "%s"' % msg)
        try:
            data = msg.data
            left = data[0]
            right = data[1]
            obj = {
                'to': 'wheel',
                'data': [left, right]
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

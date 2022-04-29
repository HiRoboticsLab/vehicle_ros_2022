#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import String


class Infrared():

    def __init__(self, callback):
        rospy.Subscriber('cmd_infrared', String, self.on_receive_msg, 10) \

        self.sender = callback

    def on_receive_msg(self, msg, args):
        rospy.logdebug('receive cmd --> infrared : "%s"' % msg)
        try:
            obj = {
                'to': 'infrared',
                'data': int(msg.data, 16)
            }
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            rospy.logerr('%s' % e)
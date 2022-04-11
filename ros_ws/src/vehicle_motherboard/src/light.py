#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import String


class Light():

    def __init__(self, callback):
        self.listener_light = rospy.Subscriber('cmd_light', String, self.on_receive_msg, 10) \

        self.sender = callback

    def on_receive_msg(self, msg, args):
        rospy.logdebug('receive cmd --> light : "%s"' % msg)
        try:
            obj = {
                'to': 'light',
                'data': msg.data
            }
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            rospy.logerr('%s' % e)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import String


class Esp():

    def __init__(self, callback):
        self.listener_esp = rospy.Subscriber('cmd_esp', String, self.on_receive_msg, 10) \

        self.sender = callback

    def on_receive_msg(self, msg, args):
        rospy.logdebug('receive cmd --> esp : "%s"' % msg)
        try:
            obj = json.loads(msg.data.replace("\'", "\""))
            obj["to"] = "esp"
            # stm32接收换行表示结尾
            json_str = json.dumps(obj) + "\r\n"
            self.sender(json_str)
        except Exception as e:
            rospy.logerr('%s' % e)

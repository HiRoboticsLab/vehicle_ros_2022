#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
from std_msgs.msg import String


class Button():

    def __init__(self):
        self.talker_button = rospy.Publisher('button', String, queue_size=10)

    def report(self, state):
        rospy.logdebug('report button : "%s"' % state)
        try:
            msg_button = String()
            msg_button.data = state
            self.talker_button.publish(msg_button)
        except Exception as e:
            rospy.logerr('%s' % e)

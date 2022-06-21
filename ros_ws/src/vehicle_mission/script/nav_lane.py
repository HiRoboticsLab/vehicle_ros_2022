#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from vision_msgs.msg import Detection2DArray
from geometry_msgs.msg import Twist
import math
import time


ctrl_frequency = 5
last_ctrl_timestamp = 0
start_ctrl_timestamp = 0


def callback(data):
    global ctrl_frequency, last_ctrl_timestamp, start_ctrl_timestamp

    for detection in data.detections:
        for result in detection.results:
            if result.id == 3:

                center_x = detection.bbox.center.x
                center_y = detection.bbox.center.y
                # rospy.loginfo('center x: %s y: %s', detection.bbox.center.x, detection.bbox.center.y)

                side_x = 320 - center_x
                side_y = 360 - center_y
                angle = math.degrees(math.atan2(side_y, side_x))
                angle = angle - 90

                print(angle)

                speed_linear = 0
                speed_angular = 0

                if abs(angle) > 50:
                    if angle < 0:
                        speed_angular = 1.0
                    elif angle > 0:
                        speed_angular = -1.0
                else:
                    speed_linear = 0.2
                    if angle < 0:
                        speed_angular = 0.5
                    else:
                        speed_angular = -0.5

                msg = Twist()

                if (time.time() - last_ctrl_timestamp) > (1 / ctrl_frequency):
                    msg.linear.x = speed_linear
                    msg.angular.z = speed_angular

                    if time.time() - start_ctrl_timestamp > 100:
                        msg.linear.x = 0
                        msg.angular.z = 0

                    pub_cmd_vel.publish(msg)
                    last_ctrl_timestamp = time.time()


if __name__ == '__main__':

    rospy.init_node('nav_lane')

    rospy.Subscriber('/detectnet/detections', Detection2DArray, callback)

    pub_cmd_vel = rospy.Publisher('/vehicle/cmd_vel', Twist, queue_size=10)

    start_ctrl_timestamp = time.time()

    rospy.spin()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from vision_msgs.msg import Detection2DArray
from geometry_msgs.msg import Twist
from tf2_msgs.msg import TFMessage
import tf
import math
import time

# 红绿灯-0、第一段障碍-1、巡线-2、第三段障碍-3
CHECK_POINT = 0
# 巡线控制频率
ctrl_frequency = 10
last_ctrl_timestamp = 0

# 路径点
points_first = [[0.58, 0.0], [1.40, 0.50], [0.15, 0.56]]
points_last = [[-0.1, -0.1], [0, 0]]

# 巡线结束的坐标
allow_position = [-1.45, 1.0]
allow_threshold = 0.2

# 导航用的数据
nav_flag, last_theta = 0, 0


def buttonEvent(data):
    global nav_flag, CHECK_POINT
    rospy.loginfo('I heard %s', data.data)
    if(data.data == 'click'):
        # 等待绿灯
        while CHECK_POINT == 0:
            print('.')
            time.sleep(0.1)
        nav_flag = 0
        do_pub()


def do_pub():
    global nav_flag, last_theta
    global CHECK_POINT

    if CHECK_POINT == 1:
        points = points_first
    if CHECK_POINT == 3:
        points = points_last

    over = len(points)

    if(nav_flag == over):
        # 如果第一阶段运行完成
        if CHECK_POINT == 1:
            CHECK_POINT = 2
        return

    want_go_point = points[nav_flag]

    # 如果不是最后一个点
    if nav_flag != over - 1:
        next_point = points[nav_flag + 1]
        delta_y = next_point[1] - want_go_point[1]
        delta_x = next_point[0] - want_go_point[0]
        last_theta = math.atan2(delta_y, delta_x)

    nav_flag = nav_flag + 1

    print("pub %s" % want_go_point)

    publish_goal(want_go_point[0], want_go_point[1], last_theta)


def publish_goal(x=0, y=0, yaw=0):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = 0
    quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)
    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]

    move_base.send_goal(goal)
    rospy.loginfo('Inital goal status: %s' %
                  GoalStatus.to_string(move_base.get_state()))
    status = move_base.get_goal_status_text()
    if status:
        rospy.loginfo(status)
    move_base.wait_for_result()
    result = GoalStatus.to_string(move_base.get_state())
    status = move_base.get_goal_status_text()
    rospy.loginfo('Final goal status: %s' % result)
    rospy.loginfo('%s' % status)
    if result == "SUCCEEDED":
        print("...")
        do_pub()


def callback_image(data):
    global ctrl_frequency, last_ctrl_timestamp, start_ctrl_timestamp
    global CHECK_POINT

    for detection in data.detections:
        for result in detection.results:
            # 绿灯
            if result.id == 2:
                if CHECK_POINT == 0:
                    CHECK_POINT = 1
            # 摄像头巡线
            if result.id == 3:
                if CHECK_POINT == 2:
                    center_x = detection.bbox.center.x
                    center_y = detection.bbox.center.y
                    # rospy.loginfo('center x: %s y: %s', detection.bbox.center.x, detection.bbox.center.y)

                    side_x = 320 - center_x
                    side_y = 360 - center_y
                    angle = math.degrees(math.atan2(side_y, side_x))
                    angle = angle - 90

                    # print(angle)

                    speed_linear = 0
                    speed_angular = 0

                    if abs(angle) > 50:
                        if angle < 0:
                            speed_angular = 1.0
                        elif angle > 0:
                            speed_angular = -1.0
                    else:
                        speed_linear = 0.05
                        if angle < 0:
                            speed_angular = 0.3
                        else:
                            speed_angular = -0.3

                    msg = Twist()

                    if (time.time() - last_ctrl_timestamp) > (1 / ctrl_frequency):
                        msg.linear.x = speed_linear
                        msg.angular.z = speed_angular

                        pub_cmd_vel.publish(msg)
                        last_ctrl_timestamp = time.time()


def callback_tf(data):
    global CHECK_POINT, allow_position, allow_threshold, nav_flag

    for transform in data.transforms:
        if transform.child_frame_id == 'base_footprint':
            position = transform.transform.translation
            if (position.x > allow_position[0] - allow_threshold) and (position.x < allow_position[0] + allow_threshold) and \
                    (position.y > allow_position[1] - allow_threshold) and (position.y < allow_position[1] + allow_threshold):
                # 如果巡线结束、则开始走最后一段
                if CHECK_POINT == 2:
                    CHECK_POINT = 3
                    nav_flag = 0
                    do_pub()


if __name__ == '__main__':

    rospy.init_node('mission')

    rospy.Subscriber('/vehicle/button', String, buttonEvent)
    rospy.Subscriber('/detectnet/detections', Detection2DArray, callback_image)
    rospy.Subscriber('/tf', TFMessage, callback_tf)

    pub_cmd_vel = rospy.Publisher('/vehicle/cmd_vel', Twist, queue_size=10)

    move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base.wait_for_server()

    rospy.spin()

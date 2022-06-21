#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf
import math


# teb
# points = [[1.40, 0.50], [0.15, 0.56]]
# dwa
points = [[1.40, 0.50], [0.15, 0.56]]
flag, last_theta= 0, 0


def buttonEvent(data):
    global flag
    rospy.loginfo('I heard %s', data.data)
    if(data.data == 'click'):
        flag = 0
        do_pub()


def do_pub():
    global flag, last_theta

    over = len(points)

    if(flag == over):
        return

    want_go_point = points[flag]

    # 如果不是最后一个点
    if flag != over - 1:
        next_point = points[flag + 1]
        delta_y = next_point[1] - want_go_point[1]
        delta_x = next_point[0] - want_go_point[0]
        last_theta = math.atan2(delta_y, delta_x)

    flag = flag + 1

    print("pub %s" % want_go_point)

    publish_goal(want_go_point[0], want_go_point[1], last_theta)


    
    # if flag == -1:
    #     cur_nav = [0, 0]
    # else:
    #     cur_nav = points[flag]

    # over = len(points)

    # if flag != over:
    #     next_nav = points[flag + 1]

    #     delta_y = next_nav[1] - cur_nav[1]
    #     delta_x = next_nav[0] - cur_nav[0]
    #     theta = math.atan2(delta_y, delta_x)
    
    #     flag = flag + 1

    #     print("pub %s" % next_nav)

    #     publish_goal(next_nav[0], next_nav[1], theta)

    


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


if __name__ == '__main__':

    rospy.init_node('nav_to_point')

    rospy.Subscriber('/vehicle/button', String, buttonEvent)

    move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    move_base.wait_for_server()

    rospy.spin()

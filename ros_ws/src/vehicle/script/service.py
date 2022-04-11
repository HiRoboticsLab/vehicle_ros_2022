#!/usr/bin/python
# -*- coding: utf-8 -*-

from vehicle.srv import param, paramResponse
import rospy
import os


# shell_path_map_build = '~/Desktop/vehicle/ros_ws/service/vehicle_map_build.sh'
# shell_path_map_save = '~/Desktop/vehicle/ros_ws/service/vehicle_map_save.sh'
# shell_path_map_navigation = '~/Desktop/vehicle/ros_ws/service/vehicle_map_navigation.sh'

# shell_build_map_path = '. ~/Desktop/vehicle/ros_ws/src/vehicle/script/buildMap.sh'
shell_build_map_path = 'roslaunch vehicle_map build.launch'


# shell_map_build_1 = 'rosrun cartographer_ros cartographer_node -configuration_directory=/home/jetbot/Desktop/vehicle/ros_ws/src/vehicle_map/config -configuration_basename=cartographer_2d.lua &'
# shell_map_build_2 = 'rosrun cartographer_ros cartographer_occupancy_grid_node -resolution 0.05 &'


# shell_map_build = '. /home/nvidia/Desktop/vehicle/ros_ws/service/vehicle_map_build.sh'

shell_map_finish_trajectory = 'rosservice call /finish_trajectory 0'
shell_map_save_pbstream = 'rosservice call /write_state "filename: \'/home/jetbot/Desktop/vehicle/ros_ws/src/vehicle_nav/map/map.pbstream\'"'
shell_map_pbstream_to_ros_map = 'rosrun cartographer_ros cartographer_pbstream_to_ros_map -pbstream_filename=/home/jetbot/Desktop/vehicle/ros_ws/src/vehicle_nav/map/map.pbstream -map_filestem=/home/jetbot/Desktop/vehicle/ros_ws/src/vehicle_nav/map/map -resolution=0.05'

shell_map_shutdown = 'rosnode kill /cartographer_node /cartographer_occupancy_grid_node'

shell_nav_start = 'roslaunch vehicle_nav navigation.launch'
shell_nav_shutdown = 'rosnode kill /cartographer_node /cartographer_occupancy_grid_node /move_base'


process_map = False
process_nav = False


def service_callback(req):
    global process_map, process_nav

    rospy.logdebug(req.cmd)

    if(("Map" in req.cmd) and process_nav):
        return paramResponse('请先退出导航模式')

    if(("Nav" in req.cmd) and process_map):
        return paramResponse('请先退出建图模式')

    # 开始建图
    if(req.cmd == 'StartBuildMap'):

        process_map = True
        # os.system(shell_map_build_1)
        # os.system(shell_map_build_2)
        os.system(shell_build_map_path)
        return paramResponse('建图结束')

    # 存图并停止建图
    if(req.cmd == 'SaveMap'):

        process_map = False
        os.system(shell_map_finish_trajectory)
        os.system(shell_map_save_pbstream)
        os.system(shell_map_pbstream_to_ros_map)
        os.system(shell_map_shutdown)
        return paramResponse('建图结束')

    # 停止建图
    if(req.cmd == 'StopBuildMap'):

        process_map = False
        os.system(shell_map_shutdown)
        return paramResponse('建图结束')

    # 开始导航
    if(req.cmd == 'StartNav'):

        process_nav = True
        os.system(shell_nav_start)
        return paramResponse('导航结束')

 # 停止导航
    if(req.cmd == 'StopNav'):

        process_nav = False
        os.system(shell_nav_shutdown)
        return paramResponse('导航结束')

    # 检查模式
    if(req.cmd == 'check'):
        result = '{}#{}'.format(process_map, process_nav)
        return paramResponse(result)


def vehicle_service():
    # os.system(shell_source_path)

    rospy.init_node('vehicle_service')

    s = rospy.Service('vehicle_service', param, service_callback)

    rospy.spin()


if __name__ == "__main__":
    vehicle_service()

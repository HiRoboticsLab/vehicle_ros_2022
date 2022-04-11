#!/bin/bash

# pwd="jetbot"

# echo $pwd | sudo -S chmod 777 /dev/ttyTHS1
# echo $pwd | sudo -S chmod 777 /dev/ttyUSB0

source /opt/ros/melodic/setup.bash

cd ~/Desktop/vehicle/ros_ws
catkin_make
source ~/Desktop/vehicle/ros_ws/devel/setup.bash

roslaunch vehicle start.launch
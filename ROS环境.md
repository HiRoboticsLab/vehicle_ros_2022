## 安装ROS
* [http://wiki.ros.org/melodic/Installation/Ubuntu](http://wiki.ros.org/melodic/Installation/Ubuntu)

```shell
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# sudo apt install curl # if you haven't already installed curl
# curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt-key add ros.asc

sudo apt update

sudo apt install ros-melodic-desktop

echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc

# 用到的库
sudo apt-get install ros-melodic-rosbridge-server

git clone https://github.com/Slamtec/rplidar_ros

sudo apt-get install python-pip
pip install pyserial

# 摄像头单独提出一个文件讲解，以下注释内容暂时不用
# sudo apt-get install gstreamer1.0-tools libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev
# sudo apt install ros-melodic-image-common
# git clone https://github.com/ros-drivers/gscam
# https://www.waveshare.net/wiki/IMX219-160_Camera
# 摄像头测试命令（需进入到桌面环境） DISPLAY=:0.0 nvgstcapture-1.0 --sensor-id=0

sudo apt install ros-melodic-cartographer-ros
sudo apt install ros-melodic-navigation

# 测试命令
roslaunch rosbridge_server rosbridge_websocket.launch
roslaunch rplidar_ros rplidar_a3.launch
rosrun tf static_transform_publisher 0 0 0 0 0 0 /laser /base_link 100

# 串口提权
sudo lsof | grep ttyTHS1
systemctl stop nvgetty
systemctl disable nvgetty

sudo cp /home/jetbot/Desktop/vehicle/ros_ws/20-myserial.rules /etc/udev/rules.d/20-myserial.rules

sudo udevadm control --reload
```

## 安装rosdep问题
```shell
sudo apt install python-rosdep

sudo mkdir -p /etc/ros/rosdep/sources.list.d

cd /etc/ros/rosdep/sources.list.d

sudo vim 20-default.list

复制以下内容
https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/sources.list.d/20-default.list

所有文件加此前缀，https://ghproxy.com/https://raw.githubusercontent.com/***


sudo vi /usr/lib/python2.7/dist-packages/rosdistro/__init__.py
为index-v4.yaml加此前缀，https://ghproxy.com/https://raw.githubusercontent.com/***


rosdep update
```

## 局域网代理
```
export https_proxy=http://192.168.31.227:7890 http_proxy=http://192.168.31.227:7890 all_proxy=socks5://192.168.31.227:7890
```

# 建图
```
cd ros_ws

source devel/setup.bash

roslaunch vehicle_map build.launch

# new terminal
rosservice call /finish_trajectory 0
rosservice call /write_state "filename: '/home/jetbot/Desktop/map.pbstream'"

cd ../
mv map.pbstream ./vehicle

# 地图转换
# rosrun cartographer_ros cartographer_pbstream_to_ros_map -pbstream_filename=/home/jetbot/Desktop/map.pbstream -map_filestem=/home/jetbot/Desktop/map -resolution=0.05


```

# 训练模型时
```
sudo systemctl stop vehicle.service

camera-capture csi://0 --input-width=640 --input-height=360

# 选择Detection
# 确定Path，并新建labels.txt，每一行添加一个分类

# 我这里选择路径为"/home/jetbot/Desktop/vehicle/datasets/", labels.txt同级

cd /home/jetbot/Desktop/vehicle/jetson-inference/python/training/detection/ssd
python3 train_ssd.py --dataset-type=voc --data=/home/jetbot/Desktop/vehicle/datasets/ --model-dir=/home/jetbot/Desktop/vehicle/datasets/model/

# 模型缩小
python3 onnx_export.py --model-dir=/home/jetbot/Desktop/vehicle/datasets/model

```

# 车道线检测，已经改为ai识别，可用可不用
```
# gui环境下使用
rosrun rqt_reconfigure rqt_reconfigure
```

# 需要补充的库
```
sudo apt-get install ros-melodic-teb-local-planner
pip install simple-pid
```
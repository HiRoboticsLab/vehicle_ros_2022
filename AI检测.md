## 人工智能
* [https://github.com/dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference)
```shell
sudo apt-get update
sudo apt-get install git cmake libpython3-dev python3-numpy
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig

# 下载模型
cd build 
./download-models.sh

# 需要安装
sudo apt install ros-melodic-vision-msgs
```

## 收集数据
```
# 打开摄像机
camera-capture csi://0 --input-width=640 --input-height=360

# 选择Detection
# 确定Path，并新建labels.txt，每一行添加一个分类

# 我这里选择路径为"/home/jetbot/Desktop/vehicle/datasets/", labels.txt同级
```

## 训练模型
```shell
cd /home/jetbot/Desktop/vehicle/jetson-inference/python/training/detection/ssd
python3 train_ssd.py --dataset-type=voc --data=/home/jetbot/Desktop/vehicle/datasets/ --model-dir=/home/jetbot/Desktop/vehicle/datasets/model/

# 模型缩小
python3 onnx_export.py --model-dir=/home/jetbot/Desktop/vehicle/datasets/model

# 测试
detectnet --model=/home/jetbot/Desktop/vehicle/datasets/model/ssd-mobilenet.onnx --labels=/home/jetbot/Desktop/vehicle/datasets/model/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes csi://0 --input-width=640 --input-height=360
```

## 初始模型放置
```shell
cd <jetson-inference>/data/networks/
tar -zxvf <model-archive-name>.tar.gz
```

## FAQ
* 挂载swap内存
https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md

* module ‘PIL.Image ‘has no attribute ‘BILINEAR‘ (2022-4-12)
```shell
pip3 uninstall pillow
pip3 install pillow==8.4.0
```

* 缺少文件mobilenet-v1-ssd-mp-0_675.pth
https://forums.developer.nvidia.com/t/jetson-nano-train-model-for-my-own-object-detection/157970
```shell
cd jetson-inference/python/training/detection/ssd
wget https://nvidia.box.com/shared/static/djf5w54rjvpqocsiztzaandq1m3avr7c.pth -O models/mobilenet-v1-ssd-mp-0_675.pth
```



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

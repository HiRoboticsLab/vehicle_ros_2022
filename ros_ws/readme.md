# 可选
# sudo chmod +x vehicle.sh

# 安装服务
sudo cp /home/jetbot/Desktop/vehicle/ros_ws/vehicle.service /etc/systemd/system/vehicle.service
sudo chmod +x /etc/systemd/system/vehicle.service
systemctl enable vehicle

systemctl start vehicle
systemctl stop vehicle
systemctl status vehicle
systemctl restart vehicle



sudo usermod -a -G dialout jetbot
sudo usermod -a -G tty jetbot
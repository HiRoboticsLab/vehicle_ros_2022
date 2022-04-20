## wifi操作
```shell
# 连接
sudo nmcli device wifi connect 'SSID' password 'PASSWORD'
# 断开
sudo nmcli connection down SSID
# 删除
sudo nmcli connection del SSID
# 查看状态
sudo nmcli connection show
sudo nmcli device status
# 开启热点
sudo nmcli dev wifi hotspot ssid 'SSID' password 'PASSWORD'
# 设置开机自动连接，下方为自动连接热点
sudo nmcli connection modify Hotspot autoconnect yes
```
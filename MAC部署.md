# 查看盘符，选physical
diskutil list external | fgrep '/dev/disk'

# 格式化，disk4需要对应更改
sudo diskutil partitionDisk /dev/disk4 1 GPT "Free Space" "%noformat%" 100%

# 刷镜像，disk4需要对应更改
unzip -p ~/Img/jetson-nano-jp461-sd-card-image.zip | sudo dd of=/dev/rdisk4 bs=1m status=progress
# 查看盘符，选physical
diskutil list external | fgrep '/dev/disk'

# 格式化，disk4需要对应更改
sudo diskutil partitionDisk /dev/disk4 1 GPT "Free Space" "%noformat%" 100%

# 刷镜像，disk4需要对应更改
unzip -p ~/Img/jetson-nano-jp461-sd-card-image.zip | sudo dd of=/dev/rdisk4 bs=1m status=progress

# 备份镜像
sudo dd if=/dev/rdisk4 conv=sync,noerror bs=1M status=progress | gzip -c > ./backup_jetson_2022.img.gz

# 恢复镜像
diskutil list disk4

diskutil umount /dev/disk4s1

gunzip -c ./backup_jetson_2022.img.gz | sudo dd of=/dev/rdisk4 bs=1m status=progress

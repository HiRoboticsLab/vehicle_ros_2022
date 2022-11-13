# slam_toolbox
```shell
# 源码方式下载的需要删除包
sudo apt-get purge ros-melodic-slam-toolbox

# 环境可能需要安装
sudo apt-get install ros-melodic-sparse-bundle-adjustment

# slam_toolbox需要修改的地方
/slam_toolbox/lib/karto_sdk/include/karto_sdk   4373行	改为+1
--- m_NumberOfRangeReadings = static_cast<kt_int32u>(math::Round((GetMaximumAngle() - GetMinimumAngle()) / GetAngularResolution()) + residual);
+++ m_NumberOfRangeReadings = static_cast<kt_int32u>(math::Round((GetMaximumAngle() - GetMinimumAngle()) / GetAngularResolution()) + 1);
```


# rf2o_laser_odometry
```shell
# https://blog.csdn.net/hiram_zhang/article/details/116220680

# CLaserOdometry2D: 295、319行，更换为
--- if (dcenter > 0.f)
+++ if (std::isfinite(dcenter) && dcenter > 0.f)

# CLaserOdometry2DNode: 126行
+++ tf_listener.waitForTransform(base_frame_id, "laser_link", ros::Time(), ros::Duration(5.0));
```


# nomachine
```shell
sudo dpkg -i nomachine_8.2.3_3_arm64.deb
```

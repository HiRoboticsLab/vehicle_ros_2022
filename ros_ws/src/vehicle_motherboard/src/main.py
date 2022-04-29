#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import rospy
import serial
import threading
from light import Light
from wheels import Wheel
from esp import Esp
from pid import PID
from button import Button
from infrared import Infrared

import subprocess

SYSTEM_PASSWORD = "jetbot"


# 临时变量
light = None
wheel = None
esp = None
pid = None


# 串口初始化
serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)


# json判断
def is_json(value):
    try:
        json_object = json.loads(value)
        return True, json_object
    except ValueError as e:
        return False


# 写串口
def write_serial(json_str):
    serial_port.write(json_str.encode())


# 读串口
def read_serial():
    while True:
        try:
            if serial_port.inWaiting() > 0:
                # 读取串口数据
                data = serial_port.readline()
                # 可以去掉b与‘符号
                # json_str = str(data, encoding="ascii")
                # print(data)
                ok, obj = is_json(data)

                if ok:
                    if 'button' in obj:
                        # print("restart wxmp")
                        # cmd = "echo '{}' | sudo -S sudo systemctl restart wxmp".format(SYSTEM_PASSWORD)     \

                        # subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)     \

                        button.report(obj['button'])

                    else:
                        array_wheel = obj['wheel']
                        wheel.report(array_wheel)

                    #     array_ypr = obj['ypr']
                    #     array_quaternion = obj['quaternion']
                    #     array_accel = obj['accel']
                    #     imu.report_ypr(array_ypr)
                    #     imu.report_imu(array_ypr, array_quaternion, array_accel)

        except Exception as e:
            print('Serial receive error')
            print(e)


# 主函数
if __name__ == '__main__':

    rospy.init_node('vehicle_motherboard', anonymous=True)
    # rate = rospy.Rate(50)

    light = Light(write_serial)
    wheel = Wheel(write_serial)
    esp = Esp(write_serial)
    pid = PID(write_serial)
    button = Button()
    infrared = Infrared(write_serial)

    # 启动串口接收
    thread = threading.Thread(target=read_serial, args=())
    # 为了解决程序退出线程不退出的问题
    thread.setDaemon(True)
    thread.start()

    rospy.spin()
    # while not rospy.is_shutdown():
    #     rate.sleep()

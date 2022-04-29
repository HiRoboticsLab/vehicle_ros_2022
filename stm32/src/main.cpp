#include <Arduino.h>
#include <ArduinoJson.h>
#include <I2Cdev.h>
#include <MPU6050_6Axis_MotionApps_V6_12.h>
#include <OneButton.h>
#include <Ticker.h>
#include <Wire.h>
#include <stdint.h>

#include "config.h"
#include "wheel.h"

void wheelAdjust();
void reportInfo();
void turnLight();
void blink();

void transmission(u_int32_t dat);

String stateTurnLight = "off";

// 定时器
Ticker timerWheelAdjust(wheelAdjust, 100);
Ticker timerTurnlight(turnLight, 500);
Ticker timerReport(reportInfo, 50);
Ticker timerBlink(blink, 125);

// 轮子（PCB引脚顺序有调整，所以最后一个均为true）
Wheel wheel1(pin_wheel_1_in1, pin_wheel_1_in2, pin_wheel_1_code1,
             pin_wheel_1_code2, true);
Wheel wheel2(pin_wheel_2_in1, pin_wheel_2_in2, pin_wheel_2_code1,
             pin_wheel_2_code2, true);
Wheel wheel3(pin_wheel_3_in1, pin_wheel_3_in2, pin_wheel_3_code1,
             pin_wheel_3_code2, false);
Wheel wheel4(pin_wheel_4_in1, pin_wheel_4_in2, pin_wheel_4_code1,
             pin_wheel_4_code2, true);

// mpu
// Quaternion q;
// uint8_t fifoBuffer[64];  // FIFO storage buffer
// VectorFloat gravity;     // [x, y, z]            gravity vector
// float ypr[3];            // [yaw, pitch, roll]
// MPU6050 mpu;
// VectorInt16 aa;
// VectorInt16 aaReal;      // [x, y, z]            gravity-free accel sensor
// measurements VectorInt16 aaWorld;

// 按键
OneButton button(pin_btn, true);

// 硬件测试模式
void testMode();
// 向上位机报告按键状态
void reportBtnClick();
void reportBtnDoubleClick();
void reportBtnPress();
String FLAG_BTN_STATE = "";
bool FLAG_REPORT_BTN = false;

// 轮子外部中断回调函数
void callbackWheel1() { wheel1.count(); }
void callbackWheel2() { wheel2.count(); }
void callbackWheel3() { wheel3.count(); }
void callbackWheel4() { wheel4.count(); }

// 轮子开外部中断
void attachAll() {
  wheel1.attach(callbackWheel1);
  wheel2.attach(callbackWheel2);
  wheel3.attach(callbackWheel3);
  wheel4.attach(callbackWheel4);
}

// 轮子关外部中断
// void detachAll() {
//   wheel1.detach();
//   wheel2.detach();
//   wheel3.detach();
//   wheel4.detach();
// }

void reportInfo() {
  DynamicJsonDocument report(512);

  if (FLAG_REPORT_BTN) {
    report["button"] = FLAG_BTN_STATE;
    FLAG_REPORT_BTN = false;
  } else {
    // report["light"] = digitalRead(pin_light) ? "off" : "on";
    // report["turnLight"] = stateTurnLight;

    // mpu.dmpGetCurrentFIFOPacket(fifoBuffer);
    // mpu.dmpGetQuaternion(&q, fifoBuffer);
    // mpu.dmpGetGravity(&gravity, &q);
    // mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

    // report["ypr"][0] = 0;
    // // 对应车辆坐标系
    // report["ypr"][1] = 0;
    // report["ypr"][2] = 0;

    // // mpu.dmpGetAccel(&aa, fifoBuffer);
    // // mpu.dmpGetLinearAccel(&aaReal, &aa, &gravity);
    // // mpu.dmpGetLinearAccelInWorld(&aaWorld, &aaReal, &q);

    // report["accel"][0] = 0;
    // report["accel"][1] = 0;
    // report["accel"][2] = 0;

    // report["quaternion"][0] = 0;
    // report["quaternion"][1] = 0;
    // report["quaternion"][2] = 0;
    // report["quaternion"][3] = 0;

    //
    report["wheel"][0] = wheel1.getDiff();  // wheel3.getCountByDir();
    report["wheel"][1] = wheel2.getDiff();  // wheel4.getCountByDir();
    report["wheel"][2] = wheel3.getDiff();  // SetpointW4;
    report["wheel"][3] = wheel4.getDiff();  // SetpointW4;
  }

  String str = "";
  serializeJson(report, str);
  Serial3.println(str);
}

unsigned char temp_light_data = 1;
bool temp_light_dir = false;

// 主板的红蓝灯
void blink() {
  if (temp_light_data == 0x01 || temp_light_data == 0x08) {
    temp_light_dir = !temp_light_dir;
  }

  if (temp_light_dir) {
    temp_light_data = temp_light_data << 1;
  } else {
    temp_light_data = temp_light_data >> 1;
  }

  digitalWrite(pin_light_D7, (temp_light_data & 0x0e));
  digitalWrite(pin_light_D8, (temp_light_data & 0x0d));
  digitalWrite(pin_light_D9, (temp_light_data & 0x0b));
  digitalWrite(pin_light_D10, (temp_light_data & 0x07));

  // digitalWrite(pin_light_D7, !digitalRead(pin_light_D7));
  // digitalWrite(pin_light_D8, !digitalRead(pin_light_D8));
  // digitalWrite(pin_light_D9, !digitalRead(pin_light_D9));
  // digitalWrite(pin_light_D10, !digitalRead(pin_light_D10));
}

// PID调整
void wheelAdjust() {
  wheel1.adjust();
  wheel2.adjust();
  wheel3.adjust();
  wheel4.adjust();
}

void initLight() {
  // 前面板灯
  pinMode(pin_light, OUTPUT);
  pinMode(pin_light_left, OUTPUT);
  pinMode(pin_light_right, OUTPUT);
  //
  digitalWrite(pin_light, HIGH);
  digitalWrite(pin_light_left, LOW);
  digitalWrite(pin_light_right, LOW);
  // 板载灯
  pinMode(pin_light_D7, OUTPUT);
  pinMode(pin_light_D8, OUTPUT);
  pinMode(pin_light_D9, OUTPUT);
  pinMode(pin_light_D10, OUTPUT);
  //
  digitalWrite(pin_light_D7, HIGH);
  digitalWrite(pin_light_D8, HIGH);
  digitalWrite(pin_light_D9, HIGH);
  digitalWrite(pin_light_D10, HIGH);
}

// 复位转向灯
void resetTurnLight() {
  digitalWrite(pin_light_left, LOW);
  digitalWrite(pin_light_right, LOW);
}

// 转向灯控制
void turnLight() {
  if (!stateTurnLight.equals("off")) {
    if (stateTurnLight.equals("on")) {
      digitalWrite(pin_light_left, !digitalRead(pin_light_left));
      digitalWrite(pin_light_right, !digitalRead(pin_light_right));
    }
    if (stateTurnLight.equals("left")) {
      digitalWrite(pin_light_left, !digitalRead(pin_light_left));
    }
    if (stateTurnLight.equals("right")) {
      digitalWrite(pin_light_right, !digitalRead(pin_light_right));
    }
  }
}

// 大灯控制
void light(bool state) { digitalWrite(pin_light, !state); }
void light() { digitalWrite(pin_light, !digitalRead(pin_light)); }

// 红外初始化
void initInfrared() {
  pinMode(pin_infrared, OUTPUT);
  digitalWrite(pin_infrared, HIGH);
}
// 红外发射
void transmission(u_int32_t dat) {
  unsigned char i, temp;
  digitalWrite(pin_infrared, LOW);
  delay(9);
  digitalWrite(pin_infrared, HIGH);
  delay(4.5);
  for (i = 0; i < 32; i++) {
    temp = (dat >> i) & 0x01;
    if (temp == 0) {  //发射0
      digitalWrite(pin_infrared, LOW);
      delayMicroseconds(560);  //延时0.56ms
      digitalWrite(pin_infrared, HIGH);
      delayMicroseconds(560);  //延时0.56ms
    }
    if (temp == 1) {  //发射1
      digitalWrite(pin_infrared, LOW);
      delayMicroseconds(560);  //延时0.56ms
      digitalWrite(pin_infrared, HIGH);
      delayMicroseconds(1690);  //延时1.69ms
    }
  }
  digitalWrite(pin_infrared, LOW);
  delayMicroseconds(560);  //延时0.56ms
  digitalWrite(pin_infrared, HIGH);
}

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);
  Serial1.println("init done");

  Serial2.begin(115200);
  Serial2.println("init done");

  Serial3.begin(115200);
  Serial3.println("init done");

  // 四个车轮PWM频率，影响声音
  analogWriteFrequency(20000);
  // 电机H桥使能
  pinMode(pin_hr8833_left, OUTPUT);
  pinMode(pin_hr8833_right, OUTPUT);
  digitalWrite(pin_hr8833_left, HIGH);
  digitalWrite(pin_hr8833_right, HIGH);

  // HAL_NVIC_SetPriority(USART3_IRQn, 3, 1);

  // mpu6050
  // Wire.setSDA(pin_mpu_sda);
  // Wire.setSCL(pin_mpu_scl);
  // Wire.begin();

  // Wire.setClock(400000);

  // bool connected = false;

  // while (!connected) {
  //   // mpu.reset();
  //   // delay(1000);
  //   mpu.initialize();
  //   delay(2000);

  //   connected = mpu.testConnection();
  //   connected ? Serial1.println("[ok] imu") : Serial1.println("[error] imu");
  // }

  // mpu.dmpInitialize();

  // mpu.CalibrateAccel(6);
  // mpu.CalibrateGyro(6);
  // mpu.PrintActiveOffsets();
  // // turn on the DMP, now that it's ready
  // Serial1.println("Enabling DMP...");
  // mpu.setDMPEnabled(true);

  // 开启码盘中断
  attachAll();

  // 初始化灯光
  initLight();

  // 初始化红外
  initInfrared();

  // 开启定时任务
  timerWheelAdjust.start();
  timerReport.start();
  timerTurnlight.start();
  timerBlink.start();

  // 按钮
  button.attachClick(reportBtnClick);
  button.attachDoubleClick(reportBtnDoubleClick);
  button.attachLongPressStart(reportBtnPress);

  // 测试模式
  if (digitalRead(pin_btn) == LOW) {
    delay(100);
    if (digitalRead(pin_btn) == LOW) {
      testMode();
    }
  }
}

String cmd = "";
DynamicJsonDocument doc(256);

void loop() {
  // 按键检测
  button.tick();
  // 灯光定时器
  timerTurnlight.update();
  timerBlink.update();
  // 车轮pid定时器
  timerWheelAdjust.update();
  // 数据上报定时器
  timerReport.update();

  if (Serial3.available()) {
    char temp = char(Serial3.read());
    cmd += temp;
    if (temp == '\n') {
      deserializeJson(doc, cmd);

      if (!doc.containsKey("to")) {
        cmd = "";
        return;
      }

      if (doc["to"] == "wheel") {
        double left = doc["data"][0];
        double right = doc["data"][1];

        double w1s = left;
        double w2s = right;
        double w3s = left;
        double w4s = right;

        wheel1.setSpeed(w1s);
        wheel2.setSpeed(w2s);
        wheel3.setSpeed(w3s);
        wheel4.setSpeed(w4s);
      }

      if (doc["to"] == "light") {
        String arg = doc["data"];
        if (arg.equals("head")) {
          light();
        }
        if (arg.equals("left")) {
          resetTurnLight();
          if (!stateTurnLight.equals("left")) {
            stateTurnLight = "left";
          } else {
            stateTurnLight = "off";
          }
        }
        if (arg.equals("right")) {
          resetTurnLight();
          if (!stateTurnLight.equals("right")) {
            stateTurnLight = "right";
          } else {
            stateTurnLight = "off";
          }
        }
        if (arg.equals("both")) {
          resetTurnLight();
          if (!stateTurnLight.equals("on")) {
            stateTurnLight = "on";
          } else {
            stateTurnLight = "off";
          }
        }
      }

      if (doc["to"] == "pid") {
        wheel1.setPID(doc["data"][0], doc["data"][1], doc["data"][2]);
        wheel2.setPID(doc["data"][0], doc["data"][1], doc["data"][2]);
        wheel3.setPID(doc["data"][0], doc["data"][1], doc["data"][2]);
        wheel4.setPID(doc["data"][0], doc["data"][1], doc["data"][2]);
      }

      if (doc["to"] == "esp") {
        // 里面已经有了\n，就不用println了
        Serial2.print(cmd);
      }

      if (doc["to"] == "infrared") {
        transmission(doc["data"]);
      }

      cmd = "";
    }
  }
}

void reportBtnClick() {
  FLAG_BTN_STATE = "click";
  FLAG_REPORT_BTN = true;
}

void reportBtnDoubleClick() {
  FLAG_BTN_STATE = "double";
  FLAG_REPORT_BTN = true;
}

void reportBtnPress() {
  FLAG_BTN_STATE = "press";
  FLAG_REPORT_BTN = true;
}

/**
 * ==============
 *   硬件灯光测试模式
 * ==============
 */
void testLight() {
  // 前面板灯
  digitalWrite(pin_light, !digitalRead(pin_light));
  digitalWrite(pin_light_left, !digitalRead(pin_light_left));
  digitalWrite(pin_light_right, !digitalRead(pin_light_right));
  // 板载灯
  digitalWrite(pin_light_D7, !digitalRead(pin_light_D7));
  digitalWrite(pin_light_D8, !digitalRead(pin_light_D8));
  digitalWrite(pin_light_D9, !digitalRead(pin_light_D9));
  digitalWrite(pin_light_D10, !digitalRead(pin_light_D10));
}

// 测试模式定时器
Ticker timerTestLight(testLight, 1000);

void testMode() {
  timerTestLight.start();
  while (1) {
    timerTestLight.update();
  }
}
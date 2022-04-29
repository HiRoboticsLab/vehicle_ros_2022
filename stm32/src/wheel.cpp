#include "wheel.h"

#include <Arduino.h>

Wheel::Wheel(uint32_t in1, uint32_t in2, uint32_t code1, uint32_t code2,
             bool direction) {
  this->pin_in1 = in1;
  this->pin_in2 = in2;
  this->pin_code1 = code1;
  this->pin_code2 = code2;
  this->dir_default = direction;

  // 解决电机引脚占用IIC被默认初始化问题，防止波形高度不够
  pinMode(code1, INPUT_PULLDOWN);
  pinMode(code2, INPUT_PULLDOWN);

  pinMode(in1, INPUT_PULLDOWN);
  pinMode(in2, INPUT_PULLDOWN);

  disable();
}

void Wheel::tick() {
  this->target += this->speed;
}

void Wheel::setSpeed(int64_t speed) {
  if (dir_default) {
    this->speed = speed * -1;
  } else {
    this->speed = speed;
  }
}

void Wheel::disable() {
  analogWrite(this->pin_in1, 0);
  analogWrite(this->pin_in2, 0);
}

void Wheel::attach(void (*callback)(void)) {
  attachInterrupt(this->pin_code1, callback, RISING);
  // attachInterrupt(pin_code2, callback, RISING);
}

// void Wheel::detach() {
//   detachInterrupt(pin_code1);
//   detachInterrupt(pin_code2);
// }

void Wheel::count() {
  int temp = digitalRead(this->pin_code2);
  if (temp > 0) {
    this->code++;
  } else {
    this->code--;
  }
}

void Wheel::adjust() {
  long currT = micros();
  float deltaT = ((float)(currT - prevT)) / (1.0e6);
  this->prevT = currT;
  // error
  this->diff = this->code - this->target;
  // derivative
  float dedt = (this->diff - this->eprev) / (deltaT);
  // integral
  this->eintegral = this->eintegral + this->diff * deltaT;
  // control signal
  float u =
      this->kp * this->diff + this->kd * dedt + this->ki * this->eintegral;
  // motor power
  float pwm = fabs(u);
  // if (pwm > 255) {
  //   pwm = 255;
  // }
  // motor direction
  if (u > 0) {
    analogWrite(this->pin_in1, pwm);
    analogWrite(this->pin_in2, 0);
  }
  if (u < 0) {
    analogWrite(this->pin_in1, 0);
    analogWrite(this->pin_in2, pwm);
  }

  this->eprev = this->diff;

  tick();
}

void Wheel::setPID(float kp, float ki, float kd) {
  this->kp = kp;
  this->ki = ki;
  this->kd = kd;
}

int Wheel::getDiff() { return this->diff; }

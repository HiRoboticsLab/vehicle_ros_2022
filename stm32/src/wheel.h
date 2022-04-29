#ifndef __WHEEL_H__
#define __WHEEL_H__

#include <stdint.h>

class Wheel {
 private:
  float kp = 1;  // 2.5;
  float ki = 0.5;
  float kd = 0.05;

  uint32_t pin_in1;
  uint32_t pin_in2;
  uint32_t pin_code1;
  uint32_t pin_code2;
  bool dir_default;
  bool is_disable = true;

  void disable();
  void enable(bool dir);
  void tick();

  long prevT = 0;
  float eprev = 0;
  float eintegral = 0;

  volatile int64_t code = 0;
  int64_t target = 0;
  int64_t speed = 0;

  int diff = 0;

 public:
  Wheel(uint32_t in1, uint32_t in2, uint32_t code1, uint32_t code2,
        bool direction);
  void setSpeed(int64_t speed);
  void attach(void (*callback)(void));
  //   void detach();
  void count();
  void adjust();
  void setPID(float kp, float ki, float kd);
  int getDiff();
};

#endif

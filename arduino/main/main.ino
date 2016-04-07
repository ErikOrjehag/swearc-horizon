#include <HalMotor.h>

void tick1();

HalMotor motor1(
  26, // R PWM
  28, // L PWM
  22, // Hal 1
  24, // Hal 2
  200, // Pulses per revolution
  tick1 // interrupt
);

void tick1() {
  motor1.tick();
}

void setup() {
  
}

void loop() {
  motor1.update();
}

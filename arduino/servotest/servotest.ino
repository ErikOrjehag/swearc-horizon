
#include <Servo.h>

Servo servo;
int servoPin = 3;

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
}

void loop() {
  float val = sin(millis() * 0.002) * 90 + 90;
  Serial.println(val);
  servo.write(val);
  delay(10);
}

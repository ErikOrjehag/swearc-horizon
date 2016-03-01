
#include <Servo.h>

Servo servo;
int servoPin = 3;
int deg = 0;

void setup() {
  Serial.begin(9600);
  servo.attach(servoPin);
}

void loop() {

  String data = "test=";
  data.concat(12.212);
  Serial.println(data);
  
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('=');

    if (command == "servo") {
      deg = Serial.parseInt();
    }
  }
  
  servo.write(deg);
  // delay(10);
}

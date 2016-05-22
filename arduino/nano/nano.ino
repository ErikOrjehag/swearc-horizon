#include <Servo.h>

int pwmPin1 = 3;
int pwmPin2 = 9;

int servoPin = 9;
int resetLiftPin = 10;
int resetElevPin = 11;

int servoLift = 80;
int servoElev = 40;
int pwm = 0;

Servo servo;

void setup() {
  Serial.begin(9600);

  //servo.attach(servoPin);

  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(resetLiftPin, INPUT_PULLUP);
  pinMode(resetElevPin, INPUT_PULLUP);

  //servo.write(180);
}

void loop() {

  readSerialInput();

  //Serial.println(pwm);

  if (pwm >= 0) {
    analogWrite(pwmPin1, pwm);
    analogWrite(pwmPin2, 0);
  } else {
    analogWrite(pwmPin1, 0);
    analogWrite(pwmPin2, -pwm);
  }
}

void readSerialInput() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('=');
    String value = Serial.readStringUntil(',');

    Serial.print(command);
    Serial.print(" ");
    Serial.println(value);

    if (command == "elev") {
      pwm = value.toInt();

    } else {
      Serial.println("Unrecognized command!");
    }
  }
}
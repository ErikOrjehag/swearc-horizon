#include <Servo.h>

int optiPin = 2;
int hallPin = 3;
int pwmPin1 = 5;
int pwmPin2 = 6;
int servoPin = 9;
int resetLiftPin = 10;
int resetElevPin = 11;

int servoLift = 80;
int servoElev = 40;

Servo servo;

void setup() {
  Serial.begin(9600);

  servo.attach(servoPin);
  pinMode(optiPin, INPUT);
  pinMode(hallPin, INPUT);
  pinMode(pwmPin1, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(resetLiftPin, INPUT_PULLUP);
  pinMode(resetElevPin, INPUT_PULLUP);
  
  servo.write(servoLift);
  //attachInterrupt(digitalPinToInterrupt(optiPin), optiInterrupt, RISING);
  //attachInterrupt(digitalPinToInterrupt(hallPin), hallInterrupt, RISING);

  analogWrite(pwmPin1, 70);
}

void loop() {
  /*Serial.print("reset lift: ");
  Serial.println(digitalRead(resetLiftPin));
  Serial.print("reset elev: ");
  Serial.println(digitalRead(resetElevPin));*/
  /*Serial.print("hall: ");
  Serial.println(digitalRead(hallPin));*/
  Serial.print("opti: ");
  Serial.println(digitalRead(optiPin));
}

void optiInterrupt() {
  //Serial.println("opti");
}

void hallInterrupt() {
  //Serial.println("hall");
}


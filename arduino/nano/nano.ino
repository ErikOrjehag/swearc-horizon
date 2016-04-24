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
int pwm = 0;

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
  
  servo.write(servoElev);
  attachInterrupt(digitalPinToInterrupt(optiPin), optiInterrupt, RISING);
  //attachInterrupt(digitalPinToInterrupt(hallPin), hallInterrupt, RISING);

  
}

int opticount = 0;

void loop() {
  /*Serial.print("reset lift: ");
  Serial.println(digitalRead(resetLiftPin));
  Serial.print("reset elev: ");
  Serial.println(digitalRead(resetElevPin));*/
  /*Serial.print("hall: ");
  Serial.println(digitalRead(hallPin));*/

  readSerialInput();
  
  if (pwm >= 0) {
    analogWrite(pwmPin1, pwm);
    analogWrite(pwmPin2, 0);
  } else {
    analogWrite(pwmPin1, 0);
    analogWrite(pwmPin2, -pwm);
  }
}

void optiInterrupt() {
  Serial.println(++opticount);
}

void hallInterrupt() {
  //Serial.println("hall");
}


void readSerialInput() {
  if (Serial.available() > 0) {  
    String command = Serial.readStringUntil('=');
    String value = Serial.readStringUntil(',');

    /*Serial.print(command);
    Serial.print(" ");
    Serial.println(value);*/
    
    if (command == "elev") {
      pwm = value.toInt();
      
    } else {
      Serial.println("Unrecognized command!");
    }
  }
}


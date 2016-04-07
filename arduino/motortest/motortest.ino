int forwardPin = 9;
int reversePin = 10;
int ledPin = 13;
int speed = 70;
int dir = 0;

int wheelForwardPin = 5;
int wheelReversePin = 6;
int wheelDir = 0;
int wheelSpeed = 255;

void setup() {  
  pinMode(forwardPin, OUTPUT);
  pinMode(reversePin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(wheelForwardPin, OUTPUT);
  pinMode(wheelReversePin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
  if (Serial.available() > 0) {  
    String command = Serial.readStringUntil('=');
    
    if (command == "arm") {
      String dirStr = Serial.readStringUntil(',');
      dir = dirStr.toInt();
    }

    if (command == "wheel") {
      String dirStr = Serial.readStringUntil(',');
      wheelDir = dirStr.toInt();
    }
  }

  if (dir == 0) {
    analogWrite(reversePin, 0);
    analogWrite(forwardPin, 0);
  } else if (dir > 0) {
    analogWrite(reversePin, 0);
    analogWrite(forwardPin, speed);
  } else {
    analogWrite(reversePin, speed);
    analogWrite(forwardPin, 0);
  }

  if (wheelDir == 0) {
    analogWrite(wheelReversePin, 0);
    analogWrite(wheelForwardPin, 0);
  } else if (wheelDir > 0) {
    analogWrite(wheelReversePin, 0);
    analogWrite(wheelForwardPin, wheelSpeed);
  } else {
    analogWrite(wheelReversePin, wheelSpeed);
    analogWrite(wheelForwardPin, 0);
  }
}

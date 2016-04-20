/*
HC-SR04 Ping distance sensor]
VCC to arduino 5v GND to arduino GND
Echo to Arduino pin 13 Trig to Arduino pin 12
Red POS to Arduino pin 11
Green POS to Arduino pin 10
560 ohm resistor to both LED NEG and GRD power rail
More info at: http://goo.gl/kJ8Gl
Original code improvements to the Ping sketch sourced from Trollmaker.com
Some code and wiring inspired by http://en.wikiversity.org/wiki/User:Dstaub/robotcar
*/

#define trigPin 13
#define echoPin 12
#define led 11
#define led2 10

const int speedOfSound = 340;
const float ms2mm = (speedOfSound / 1000.0);

void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(trigPin, LOW);
  digitalWrite(led, LOW);
  digitalWrite(led2, LOW);
}

void loop() {
  long duration, distance;
  // Ensure clean HIGH pulse by first giving a short LOW
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(25);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) * ms2mm;
  
  if (distance < 100) {
    digitalWrite(led,HIGH);
    digitalWrite(led2,LOW);
  } else {
    digitalWrite(led,LOW);
    digitalWrite(led2,HIGH);
  }
  
  Serial.print(distance);
  Serial.println(" mm");
  
  delay(10);
}

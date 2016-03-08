#include <NewPing.h>

#define trigPin 13
#define echoPin 12
#define led 11
#define led2 10
#define maxDist 50 // cm

NewPing sonar(trigPin, echoPin, maxDist);

void setup() {
  Serial.begin (9600);
}

void loop() {
  int distance = sonar.ping_cm();
  Serial.print(distance);
  Serial.println(" cm");
  delay(50);
}

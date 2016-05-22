
int ppr = 1340;
int revolutions = 20;
int pulses = ppr * revolutions;

int m1PwmPin = 5; // 4
int m2PwmPin = 11; // 10
int m3PwmPin = 9; // 8
int m4PwmPin = 7; // 6

int m1SensorPin = 2;
int m2SensorPin = 21;
int m3SensorPin = 20;
int m4SensorPin = 18;

int n1 = 0;
int n2 = 0;
int n3 = 0;
int n4 = 0;

void setup() {
  pinMode(m1PwmPin, OUTPUT);
  pinMode(m2PwmPin, OUTPUT);
  pinMode(m3PwmPin, OUTPUT);
  pinMode(m4PwmPin, OUTPUT);
  pinMode(m1SensorPin, INPUT);
  pinMode(m2SensorPin, INPUT);
  pinMode(m3SensorPin, INPUT);
  pinMode(m4SensorPin, INPUT);
  //attachInterrupt(digitalPinToInterrupt(m1SensorPin), interrupt1, RISING);
  //attachInterrupt(digitalPinToInterrupt(m2SensorPin), interrupt2, RISING);
  //attachInterrupt(digitalPinToInterrupt(m3SensorPin), interrupt3, RISING);
  //attachInterrupt(digitalPinToInterrupt(m4SensorPin), interrupt4, RISING);
  //analogWrite(m1PwmPin, 255);
  analogWrite(m2PwmPin, 100);
  //analogWrite(m3PwmPin, 255);
  //analogWrite(m4PwmPin, 255);
}

void interrupt1() {
  if (n1++ > pulses) {
    analogWrite(m1PwmPin, 0);
  }
}

void interrupt2() {
  n2++;
  Serial.println(n2);
  //if (n2 > pulses) {
  //  analogWrite(m2PwmPin, 0);
  //}
}

void interrupt3() {
  if (n3++ > pulses) {
    analogWrite(m3PwmPin, 0);
  }
}

void interrupt4() {
  if (n4++ > pulses) {
    analogWrite(m4PwmPin, 0);
  }
}

void loop() {
  
}





int pin = 2;
int angle = 0;
unsigned long lastTime = millis();

void counter() {
  if (millis() - lastTime > 1) {
    angle += 360 / 30 / 2;
    lastTime = millis();
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(pin), counter, CHANGE);
}

void loop() {
  Serial.print("angle: ");
  Serial.println(angle);
  delay(10);
}

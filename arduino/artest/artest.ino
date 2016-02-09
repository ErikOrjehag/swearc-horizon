
const int photoPin = 0;
const int ledPin = 9;

int brightness = 0;

void setup(void) {
  Serial.begin(9600);
}

void loop(void) {
  int reading = analogRead(photoPin);

  // Send data to computer.
  String data = "reading=";
  data.concat(reading);
  Serial.println(data);

  // Recieve commands from computer.
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('=');

    if (command == "brightness") {
      brightness = Serial.parseInt();
    }
  }

  analogWrite(ledPin, brightness);

  delay(5);
}


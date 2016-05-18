#include <HalMotor.h>
#include <Servo.h>

// Interrupt ports on mega are: 2, 3, 18, 19, 20, 21
// Interrupt ports on nano are: 2, 3

// Pulses per revolution
int ppr = 1340;


// This is called forward declaseration of functions.
void tickFL();
void tickFR();
void tickBL();
void tickBR();

HalMotor motorFL(6, 7, 18, ppr, tickFL);
HalMotor motorFR(5, 4, 2, ppr, tickFR);
HalMotor motorBL(8, 9, 20, ppr, tickBL);
HalMotor motorBR(11, 10, 21, ppr, tickBR);

void tickFL() { motorFL.tick(); }
void tickFR() { motorFR.tick(); }
void tickBL() { motorBL.tick(); }
void tickBR() { motorBR.tick(); }

int readSensorsTs = millis();

// Camera servo
int servoPin = 44;
Servo servo;

// Start button
int startPin = 32;

// Blue LED lights under the robot.
bool lightCmdOn = false;
int lightPin = 22;
long lightTimer = millis();
bool lightTimerOn = false;

// Sonar sensors
int lSonarTrigPin = 24;
int lSonarEchoPin = 25;
int rSonarTrigPin = 26;
int rSonarEchoPin = 27;
int dSonarTrigPin = 28;
int dSonarEchoPin = 29;
int fSonarTrigPin = 30;
int fSonarEchoPin = 31;
const int speedOfSound = 340;
const float ms2mm = (speedOfSound / 1000.0);

void setup() {
  Serial.begin(9600);
  pinMode(lightPin, OUTPUT);

  pinMode(dSonarTrigPin, OUTPUT);
  pinMode(dSonarEchoPin, INPUT);
  pinMode(lSonarTrigPin, OUTPUT);
  pinMode(lSonarEchoPin, INPUT);
  pinMode(rSonarTrigPin, OUTPUT);
  pinMode(rSonarEchoPin, INPUT);
  pinMode(fSonarTrigPin, OUTPUT);
  pinMode(fSonarEchoPin, INPUT);

  pinMode(startPin, INPUT_PULLUP);
  servo.attach(servoPin);
}

void loop() {
  readSerialInput();

  if (millis() - readSensorsTs > 100) {
    readSonar("dsonar", dSonarTrigPin, dSonarEchoPin, 0);
    readSonar("lsonar", lSonarTrigPin, lSonarEchoPin, 7);
    readSonar("rsonar", rSonarTrigPin, rSonarEchoPin, 10);
    readSonar("fsonar", fSonarTrigPin, fSonarEchoPin, 0);
    readButtons();
    readSensorsTs = millis();
  }

  motorFL.update();
  motorFR.update();
  motorBL.update();
  motorBR.update();

  if (millis() - lightTimer > 300) {
    lightTimerOn = !lightTimerOn;
    lightTimer = millis();
    digitalWrite(lightPin, lightTimerOn && lightCmdOn);
  }
}

void readSerialInput() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('=');
    String value = Serial.readStringUntil(',');

    Serial.print(command);
    Serial.print(" ");
    Serial.println(value);

    if (command == "rspeed") {
      int rpm = value.toInt();
      motorFR.setRPM(rpm);
      motorBR.setRPM(rpm);

    } else if (command == "lspeed") {
      int rpm = value.toInt();
      motorFL.setRPM(rpm);
      motorBL.setRPM(rpm);

    } else if (command == "light") {
      lightCmdOn = (value == "True");

    } else if (command == "servo") {
      servo.write(value.toInt());

    } else {
      Serial.println("Unrecognized command!");
    }
  }
}

void readSonar(String id, int trigPin, int echoPin, int offset) {
  long duration, distance;
  String data;

  // Ensure clean HIGH pulse by first giving a short LOW
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(25);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distance = (duration / 2) * ms2mm;

  if (distance != 0 && distance != 1) {
    data = id;
    data.concat("=");
    data.concat(distance + offset);
    Serial.println(data);
  }
}

void readButtons() {
  int button = digitalRead(startPin) == 0 ? 1 : 0;
  String data = "start=";
  data.concat(button);
  Serial.println(data);
}
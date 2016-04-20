#include <HalMotor.h>

// Interrupt ports on mega are: 2, 3, 18, 19, 20, 21
// Interrupt ports on nano are: 2, 3

// Pulses per revolution
int ppr = 1340;

// This is called forward declaration of functions.
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

// Blue LED lights under the robot.
bool lightCmdOn = false;
int lightPin = 22;
long lightTimer = millis();
bool lightTimerOn = false;

void setup() {
  Serial.begin(9600);
  pinMode(lightPin, OUTPUT);
  //motorBR.setRPM(20);
}

void loop() {
  readSerialInput();
  
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
      
    } else {
      Serial.println("Unrecognized command!");
    }
  }
}


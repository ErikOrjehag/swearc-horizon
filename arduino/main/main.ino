#include <HalMotor.h>

// Available interrupt ports on mega are: 2, 3, 18, 19, 20, 21

// Pulses per revolution
int ppr = 1326;

// This is called forward declaration of functions.
void tickFL();
void tickFR();
void tickBL();
void tickBR();

HalMotor motorFL(6, 7, 18, ppr, tickFL);
HalMotor motorFR(13, 12, 20, ppr, tickFR);
HalMotor motorBL(8, 9, 19, ppr, tickBL);
HalMotor motorBR(11, 10, 21, ppr, tickBR);

void tickFL() { motorFL.tick(); }
void tickFR() { motorFR.tick(); }
void tickBL() { motorBL.tick(); }
void tickBR() { motorBR.tick(); }

void setup() {
  Serial.begin(9600);
  motorFL.setRPM(10);
  motorFR.setRPM(10);
  motorBL.setRPM(10);
  motorBR.setRPM(10);
}

void loop() {
  motorFL.update();
  motorFR.update();
  motorBL.update();
  motorBR.update();
}

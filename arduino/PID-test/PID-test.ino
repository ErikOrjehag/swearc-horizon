
#include <PID_v1.h>

const int SENSORPIN_ORANGE = 2;
const int SENSORPIN_BLACK = 3; 
const int LMOTOR_IN3 = 7;
const int LMOTOR_IN4 = 8;
const int LMOTOR_PWM = 9;
const int PULSES_PER_REVOLUTION = 200;
unsigned long timeCount;
unsigned long timeSinceUpdate;
double goalTimeCount;
double currTimeCount;
double currRPM;
double currPWM;
double goalRPM;
int counter;
float lMotorMaxRotation;
PID myPID(&currRPM, &currPWM, &goalRPM, 10,10,0, DIRECT);  //PID default range = 0 - 255 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogWrite(LMOTOR_PWM, 150);
  attachInterrupt(digitalPinToInterrupt(SENSORPIN_ORANGE), tick, FALLING);
  counter = 0;
  lMotorMaxRotation = 0;
  timeCount = 0;
  currPWM = 100;
  timeSinceUpdate = 0;
  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(50);

  //goalTimeCount = rpmToMillisPerPulse(goalRPM);
  //goalTimeCount = rpmToMillisPerPulse(10);
  goalRPM = 10;
  Serial.println(goalTimeCount);
  digitalWrite(LMOTOR_IN3, HIGH);
  digitalWrite(LMOTOR_IN4, LOW);
}

void loop() {
  boolean hasCompute = myPID.Compute();
  if (millis() - timeSinceUpdate > 200){
    currTimeCount = 200;
    currRPM = 0;
  }
  if (hasCompute){
    analogWrite(LMOTOR_PWM, currPWM);
    Serial.print(currPWM);
    Serial.print("     RPM:   ");
    Serial.println(currRPM);
    if (currPWM == 255){
      Serial.println("MAXED OUT!!");
    }
  }
}

float testMaxRpm(){
  analogWrite(LMOTOR_PWM, 255);
  delay(1000);
  return millisPerPulseToRPM(currTimeCount);
}

float rpmToMillisPerPulse(double rpm){
  if (rpm == 0){
    return 0;
  }
  else{
    return ((60 / rpm) / PULSES_PER_REVOLUTION) * 1000;
  }
}

float millisPerPulseToRPM(double milli){
  return 60 / ((milli * PULSES_PER_REVOLUTION) / 1000);
}

void tick(){
  currTimeCount = millis() - timeCount;
  currRPM = millisPerPulseToRPM(currTimeCount);

  timeSinceUpdate = millis();
  timeCount = millis();
}



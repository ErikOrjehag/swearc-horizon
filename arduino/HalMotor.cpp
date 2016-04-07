#include "Arduino.h"
#include "HalMotor.h"

HalMotor::HalMotor(int RPin, int LPin, int SPin1, int SPin2, int pulsesPerRev, void (*interrupt)()) {
	pinMode(RPin, OUTPUT);
	pinMode(LPin, OUTPUT);
	pinMode(SPin1, INPUT);
	pinMode(SPin2, INPUT);
	_RPin = RPin;
	_LPin = LPin;
	_SPin1 = SPin1;
	_SPin2 = SPin2;
	_pulsesPerRev = pulsesPerRev;
	pid = new PID(&_currRPM, &_currPWM, &_goalRPM, 10, 10, 0, DIRECT);
	analogWrite(RPin, 150);
	attachInterrupt(digitalPinToInterrupt(SPin1), interrupt, FALLING);
	pid->SetMode(AUTOMATIC);
	pid->SetSampleTime(50);
}

HalMotor::~HalMotor() {
	delete pid;
}

void HalMotor::drive(int pwm) {
	
}

void HalMotor::update() {
	boolean hasCompute = pid->Compute();
	
	if (millis() - _lastTickTimestamp > _freezeTimeMs) {
		_currRPM = 0;
	}

	if (hasCompute) {
		analogWrite(_RPin, _currPWM);
	}
}

void HalMotor::tick() {
	double peakToPeakTime = millis() - _lastTickTimestamp;
	_currRPM = millisPerPulseToRPM(peakToPeakTime);
	_lastTickTimestamp = millis();
}

float HalMotor::millisPerPulseToRPM(double millis) {
	return 60 / ( ( millis * _pulsesPerRev ) / 1000 );
}
#include "Arduino.h"
#include "HalMotor.h"

HalMotor::HalMotor(int RPin, int LPin, int SPin, int pulsesPerRev, void (*interrupt)()) {
	pinMode(RPin, OUTPUT);
	pinMode(LPin, OUTPUT);
	pinMode(SPin, INPUT);
	_RPin = RPin;
	_LPin = LPin;
	_SPin = SPin;
	_pulsesPerRev = pulsesPerRev;
	pid = new PID(&_currRPM, &_currPWM, &_goalRPM, 2, 8, 0, DIRECT);
	analogWrite(RPin, 150);
	attachInterrupt(digitalPinToInterrupt(SPin), interrupt, FALLING);
	pid->SetMode(AUTOMATIC);
	pid->SetSampleTime(50);
}

HalMotor::~HalMotor() {
	delete pid;
}

void HalMotor::setRPM(int rpm) {
	if (rpm < 0) {
		_reverse = true;
		_goalRPM = -rpm;
	} else {
		_reverse = false;
		_goalRPM = rpm;
	}
}

void HalMotor::update() {
	boolean hasCompute = pid->Compute();
	
	if (millis() - _lastTickTimestamp > _freezeTimeMs) {
		_currRPM = 0;
	}

	if (hasCompute) {
		//Serial.println((_goalRPM == 0) ? 0 : _currPWM);
		analogWrite(_reverse ? _RPin : _LPin, 0);
		analogWrite(_reverse ? _LPin : _RPin, (_goalRPM == 0) ? 0 : _currPWM);
	}
}

void HalMotor::tick() {
	unsigned long peakToPeakTime = millis() - _lastTickTimestamp;
	_lastTickTimestamp = millis();
	//Serial.println(peakToPeakTime);
	// Prevent division with zero.
	//if (peakToPeakTime > 0) {
		_currRPM = millisPerPulseToRPM(peakToPeakTime);
	//}
}

float HalMotor::millisPerPulseToRPM(double millis) {
	return 60 / ( ( millis * _pulsesPerRev ) / 1000 );
}
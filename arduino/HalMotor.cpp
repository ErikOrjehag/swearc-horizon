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
	_goalRPM = rpm;
}

void HalMotor::update() {
	boolean hasCompute = pid->Compute();
	
	if (millis() - _lastTickTimestamp > _freezeTimeMs) {
		_currRPM = 0;
	}

	if (hasCompute) {
		analogWrite(_RPin, _currPWM);

		Serial.print("_currRPM: ");
		Serial.print(_currRPM);
		Serial.print(", _currPWM: ");
		Serial.println(_currPWM);
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
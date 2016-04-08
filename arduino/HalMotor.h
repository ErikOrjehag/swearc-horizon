#ifndef HalMotor_h
#define HalMotor_h

#include "Arduino.h"
#include <PID_v1.h>

class HalMotor {

public:
	HalMotor(int RPin, int LPin, int SPin, int pulsesPerRev, void (*interrupt)());
	~HalMotor();
	void setRPM(int pwm);
	void update();
	void tick();

private:
	float millisPerPulseToRPM(double millis);
	int _RPin;
	int _LPin;
	int _SPin;
	int _pulsesPerRev;
	const unsigned int _freezeTimeMs = 200;
	unsigned long _lastTickTimestamp = 0;
	double _currRPM = 0;
	double _currPWM = 0;
	double _goalRPM = 0;
	PID *pid;

};

#endif
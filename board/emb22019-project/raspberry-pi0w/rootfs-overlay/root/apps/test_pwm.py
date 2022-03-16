#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

allDirPins = [5, 6, 9, 10, 11, 13];
allSpdPins = [10, 13];
rightDirPins = [5, 6];
rightSpdPin = 10;
leftDirPins = [9, 11];
leftSpdPin = 13;

GPIO.setmode(GPIO.BCM);
GPIO.setup(allDirPins, GPIO.OUT, initial=GPIO.LOW);
rightSpd = GPIO.PWM(rightSpdPin, 500);
leftSpd = GPIO.PWM(leftSpdPin, 500);
GPIO.output(rightDirPins, (GPIO.LOW, GPIO.HIGH));
GPIO.output(leftDirPins, (GPIO.HIGH, GPIO.LOW));
rightSpd.start(40);
leftSpd.start(40);
input('Press return to stop:');
rightSpd.stop();
leftSpd.stop();
GPIO.cleanup();

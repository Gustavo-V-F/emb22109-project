#!/usr/bin/env python
# coding: utf-8

# In[1]:

from timeit import default_timer as timer 
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2
 
def clockwise():
    GPIO.output(rightDirPins, (GPIO.HIGH, GPIO.LOW));
    GPIO.output(leftDirPins, (GPIO.LOW, GPIO.HIGH));
    return;

def counter_clockwise():
    GPIO.output(rightDirPins, (GPIO.LOW, GPIO.HIGH));
    GPIO.output(leftDirPins, (GPIO.HIGH, GPIO.LOW));
    return;

def pwm_start(duty):
    rightSpd.start(float(duty));
    leftSpd.start(float(duty));
    return;

def pwm_stop():
    rightSpd.stop();
    leftSpd.stop();
    return;

def pwm_set_duty(duty):
    rightSpd.ChangeDutyCycle(float(duty));
    leftSpd.ChangeDutyCycle(float(duty));
    return;

allDirPins = [5, 6, 9, 10, 11, 13];
allSpdPins = [10, 13];
rightDirPins = [5, 6];
rightSpdPin = 10;
leftDirPins = [9, 11];
leftSpdPin = 13;
a = -1;
duty = 0;
started = False;

try:
    camera = PiCamera();
    camera.awb_mode = 'auto';
    camera.resolution = (640, 480);
    camera.framerate = 24;
    camera.rotation = 270;
    rawCapture = PiRGBArray(camera, size=(640,480));
except:
    print("Failed to setup PiCamera!");
    exit();

try:
    GPIO.setmode(GPIO.BCM);
    GPIO.setup(allDirPins, GPIO.OUT, initial=GPIO.LOW);
    rightSpd = GPIO.PWM(rightSpdPin, 500);
    leftSpd = GPIO.PWM(leftSpdPin, 500);
    pwm_start(duty);
except:
    print("Failed to setup GPIO or PWM!");
    pwm_stop();
    GPIO.cleanup();
    exit();

time.sleep(2);
start = timer();

#try:
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Convert to grayscale.
    gray = cv2.cvtColor(frame.array, cv2.COLOR_BGR2GRAY);

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (5, 5));

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 23, param1 = 60, param2 = 38, minRadius = 60, maxRadius = 133); # 23, 60, 38, 60, 133

    # Draw circles that are detected.
    if detected_circles is not None:
        duty = 0;
        pwm_set_duty(duty);
        time.sleep(0.1);

        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles));

        pt = max(detected_circles[0], key=lambda e : e[2]);
        
        a, b, r = pt[0], pt[1], pt[2];
        
        print("Circle found at ("+str(a)+";"+str(b)+") with radius of "+str(r)+".");
        
        try:
            # Draw the circumference of the circle.
            cv2.circle(frame.array, (a, b), r, (0, 255, 0), 2);

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(frame.array, (a, b), 1, (0, 0, 255), 3);
            cv2.imwrite("frame.jpg", frame.array);    
        except:
            print("frame.jpg may be corrupted or not saved.")    
    elif timer() - start >= 0.01 and duty != 0:
        duty = 0;
        pwm_set_duty(duty);
        started = False;
        a = -1;
        time.sleep(0.1);
    else:
        print("No circles detected!")
        if a != -1:
            if a >= 366:
                if not started:
                    start = timer();
                    started = True;
                duty = 40;
                clockwise();
                pwm_set_duty(duty);
                print("Turning clockwise!");
            elif a <= 266:
                if not started:
                    start = timer();
                    started = True;
                duty = 40;
                counter_clockwise();
                pwm_set_duty(duty);
                print("Turning counter clockwise!");

    rawCapture.truncate(0);
#except:
#    print('Program stopped.');
#    pwm_stop();
#    GPIO.cleanup();
#    exit();

pwm_stop();
GPIO.cleanup();

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RUNNING = True

red = 2
green = 3
blue = 4

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100

RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)


def green_on(time_sleep_coef):
    RED.start(0)
    GREEN.start(100)
    BLUE.start(0)
    time.sleep(10 * time_sleep_coef - 3)
    green_blink()


def green_blink():
    i = 0
    while i < 3:
        RED.start(0)
        GREEN.start(0)
        BLUE.start(0)
        time.sleep(0.5)
        GREEN.start(100)
        time.sleep(0.5)
        i += 1


def yellow_on():
    RED.start(50)
    GREEN.start(50)
    BLUE.start(0)
    time.sleep(3)


def red_on(time_sleep_coef):
    RED.start(100)
    GREEN.start(0)
    BLUE.start(0)
    time.sleep(10 * time_sleep_coef)


def traffic_light():
    time_sleep_coef = 1

    red_on(time_sleep_coef)
    yellow_on()
    green_on(time_sleep_coef)
    yellow_on()


try:
    while RUNNING:
        traffic_light()
except KeyboardInterrupt:
    RUNNING = False
    GPIO.cleanup()

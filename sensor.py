#!/usr/bin/python3

import RPi.GPIO as gpio
import time
from threading import Lock

if gpio.getmode() is None:
    gpio.setmode(gpio.BCM)

left = 19
right = 16
trigger = 22
echo = 27

def has_obstacle() -> (bool, bool):
    global left
    global right

    return gpio.input(left) == 0, gpio.input(right) == 0

def front_distance() -> float:
    global trigger
    global echo

    gpio.output(trigger, gpio.HIGH)
    time.sleep(0.0005)
    gpio.output(trigger, gpio.LOW)

    while not gpio.input(echo):
        continue
    t = time.time()
    while gpio.input(echo):
        continue
    return (time.time()-t) * 340 / 2

gpio.setup(left, gpio.IN, gpio.PUD_UP)
gpio.setup(right, gpio.IN, gpio.PUD_UP)
gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN, gpio.PUD_UP)

if __name__ == '__main__':
    while True:
        print('(left, right): {}, front: {}m'.format(
            has_obstacle(), front_distance()))
        time.sleep(1)



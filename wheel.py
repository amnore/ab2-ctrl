#!/usr/bin/python3

import RPi.GPIO as gpio
from time import sleep

if gpio.getmode() is None:
    gpio.setmode(gpio.BCM)

wheel_port = [
    (12, 13, 6),
    (20, 21, 26)
]
wheel_speed = []

def wheel_set(speed: [float], forward = True):
    assert(len(speed) == 2)
    global wheel_port
    global wheel_speed
    for s, (p1, p2, ct), pwm in zip(speed, wheel_port, wheel_speed):
        if s >= 0:
            gpio.output((p1, p2), (0, 1))
        else:
            gpio.output((p1, p2), (1, 0))
            s = -s
        pwm.ChangeDutyCycle(s * 100)


for (p1, p2, ct) in wheel_port:
    gpio.setup((p1, p2, ct), gpio.OUT)
    pwm = gpio.PWM(ct, 1000)
    wheel_speed.append(pwm)
    pwm.start(0)

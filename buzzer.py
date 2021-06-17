#!/usr/bin/python3

import RPi.GPIO as gpio

buzzer = 4

if gpio.getmode() == None:
    gpio.setmode(gpio.BCM)

def buzzer_set(enabled = True):
    if enabled:
        gpio.output(buzzer, gpio.HIGH)
    else:
        gpio.output(buzzer, gpio.LOW)

gpio.setup(buzzer, gpio.OUT)

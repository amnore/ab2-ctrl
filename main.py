#!/usr/bin/python3

import ir
import wheel
import strip
import sensor
import buzzer
import atexit
import RPi.GPIO as gpio
import time

wheel_speed = (0, 0)
stop_distance = 0.2

def wheel_control(key, status):
    global wheel_speed
    global stop_distance
    speed_table = {
            '2': (0.5, 0.5),
            '4': (-0.15, 0.15),
            '6': (0.15, -0.15),
            '8': (-0.5, -0.5)
            }

    if status == 'down':
        if key == '2' and sensor.front_distance() < stop_distance:
            return
        wheel_speed = speed_table[key]
        wheel.wheel_set(wheel_speed)
    else:
        wheel_speed = (0, 0)
        wheel.wheel_set(wheel_speed)

def avoid_obstacle(key, status):
    assert key == '2' and status == 'repeat'

    global wheel_speed
    global stop_distance
    if wheel_speed[0] > 0 and wheel_speed[1] > 0 and sensor.front_distance() < stop_distance:
        wheel_speed = (-0.2, -0.2)
        wheel.wheel_set(wheel_speed)
    elif wheel_speed[0] < 0 and wheel_speed[1] < 0:
        wheel_speed = (0, 0)
        wheel.wheel_set(wheel_speed)

def buzzer_control(key, status):
    if status == 'down':
        buzzer.buzzer_set(True)
    elif status == 'up':
        buzzer.buzzer_set(False)

strip.strip_set(True)
strip_enabled = True

def strip_control(key, status):
    global strip_enabled
    if status == 'down':
        strip_enabled = not strip_enabled
        strip.strip_set(strip_enabled)

keys = ['2', '4', '6', '8']
states = ['up', 'down']
for k in keys:
    for s in states:
        ir.ir_add_handler(k, s, wheel_control)

ir.ir_add_handler('2', 'repeat', avoid_obstacle)

ir.ir_add_handler('5', 'down', buzzer_control)
ir.ir_add_handler('5', 'up', buzzer_control)
ir.ir_add_handler('play', 'down', strip_control)

def cleanup():
    strip.strip_set(False)
    time.sleep(0.1)

atexit.register(cleanup)

while True:
    time.sleep(1)


#!/usr/bin/python3

from neopixel import Adafruit_NeoPixel, Color
from threading import Thread
from time import sleep

strip = Adafruit_NeoPixel(
        4, # led count
        18, # led pin
        800000, # led freq
        5, # dma chan 
        False, # invert signal
        255 # brightness
        )
strip_enable = False

def strip_loop():
    loop_cnt = 0
    colors = [
            Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255),
            Color(255, 255, 0), Color(255, 0, 255), Color(0, 255, 255)
            ]
    global strip_enable

    strip.begin()
    while True:
        # print(strip_enable)
        if strip_enable == True:
            for i in range(4):
                strip.setPixelColor(i, colors[(i+loop_cnt)%len(colors)])
        else:
            for i in range(4):
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        loop_cnt = loop_cnt + 1
        sleep(0.1)

def strip_set(enable = True):
    global strip_enable
    strip_enable = enable

strip_thread = Thread(target=strip_loop)
strip_thread.start()

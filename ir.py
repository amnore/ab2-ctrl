#!/usr/bin/python3

import os
from threading import Thread
import time
import RPi.GPIO as gpio

if gpio.getmode() is None:
    gpio.setmode(gpio.BCM)

ir_table = {
        69: 'ch-', 70: 'ch', 71: 'ch+',
        68: 'prev', 64: 'next', 67: 'play',
        7: 'vol-', 21: 'vol+', 9: 'eq',
        22: '0', 25: '100+', 13: '200+',
        12: '1', 24: '2', 94: '3',
        8: '4', 28: '5', 90: '6',
        66: '7', 82: '8', 74: '9'
        }
ir_handlers = {}

IR = 17
gpio.setup(IR,gpio.IN)

def getkey():
    global IR
    if gpio.input(IR) == 0:
            count = 0
            while gpio.input(IR) == 0 and count < 200:  #9ms
                    count += 1
                    time.sleep(0.00006)
            if(count < 10):
                    return;
            count = 0
            while gpio.input(IR) == 1 and count < 80:  #4.5ms
                    count += 1
                    time.sleep(0.00006)

            idx = 0
            cnt = 0
            data = [0,0,0,0]
            for i in range(0,32):
                    count = 0
                    while gpio.input(IR) == 0 and count < 15:    #0.56ms
                            count += 1
                            time.sleep(0.00006)
                            
                    count = 0
                    while gpio.input(IR) == 1 and count < 40:   #0: 0.56mx
                            count += 1                               #1: 1.69ms
                            time.sleep(0.00006)
                            
                    if count > 7:
                            data[idx] |= 1<<cnt
                    if cnt == 7:
                            cnt = 0
                            idx += 1
                    else:
                            cnt += 1
#		print data
            if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
                    return data[2]
            else:
                    # print("repeat")
                    return "repeat"

def loop_handle_input():
    global ir_handlers
    global ir_table

    prev = None
    prev_time = time.time()
    up_threshold = 0.1
    while True:
        key = getkey()

        if key is None:
            if prev is not None and time.time() - prev_time >= up_threshold:
                # print('%s up' % prev)
                if (prev, 'up') in ir_handlers:
                    for h in ir_handlers[prev, 'up']:
                        h(prev, 'up')
                prev = None
            continue

        if key == 'repeat':
            prev_time = time.time()
            if (prev, 'repeat') in ir_handlers:
                for h in ir_handlers[prev, 'repeat']:
                    h(prev, 'repeat')
            continue

        keystr = ir_table[key]
        if prev == keystr:
            continue

        # print('%s up, %s down' %(prev, keystr))
        if (prev, 'up') in ir_handlers:
            for h in ir_handlers[prev, 'up']:
                h(prev, 'up')
        if (keystr, 'down') in ir_handlers:
            for h in ir_handlers[keystr, 'down']:
                h(keystr, 'down')
        prev = keystr
        prev_time = time.time()

def ir_add_handler(key: str, status: str, handler):
    global ir_handlers
    global ir_table

    assert key in ir_table.values() and status in ['up', 'down', 'repeat']
    if (key, status) not in ir_handlers:
        ir_handlers[(key, status)] = []
    ir_handlers[(key, status)].append(handler)

ir_thread = Thread(target=loop_handle_input)
ir_thread.start()

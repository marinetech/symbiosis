#!/usr/bin/python3

import time
import sys
import RPi.GPIO as GPIO

up_relays = ['27', '22', '10', '9']
down_relays = ['23', '24', '25', '17']
ops = ['up', "down", "off"]

def show_usage_and_exit():
    print("Usage:")
    print("\t" + sys.argv[0] + " [up | down | off]")
    exit()

def init_gpio():
    # to use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BCM)

    # disable 'channel is already in use' warnings
    GPIO.setwarnings(False)

    # GPIO Map
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)

    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)

def parse_args():
    if len(sys.argv) != 2:
        req_op = "off"
    else:
        req_op = sys.argv[1].lower()

    if req_op not in ops:
        print("-E- unknown operation: " + req_op)
        req_op = None

    return req_op


#------------------- Main Body ------------------#

req_op = parse_args()
if req_op is None:
    show_usage_and_exit()
init_gpio()

if req_op == "off":
    for relay in up_relays:
        GPIO.output(int(relay), GPIO.HIGH)
    for relay in down_relays:
        GPIO.output(int(relay), GPIO.HIGH)
elif req_op == "up":
    for relay in down_relays:
        GPIO.output(int(relay), GPIO.HIGH)
    for relay in up_relays:
        GPIO.output(int(relay), GPIO.LOW)
else: # req_op == "down"
    for relay in up_relays:
        GPIO.output(int(relay), GPIO.HIGH)
    for relay in down_relays:
        GPIO.output(int(relay), GPIO.LOW)

#!/usr/bin/python3r

import time
import sys
import RPi.GPIO as GPIO

relays = ['27', '22', '10', '9']
ops = ['on', "off"]

print("relay 22 is modem")
relay = input("Relay " + str(relays) + "? ")
if relay not in relays:
    print("-E- unknown relay: " + relay)
    exit()

op = input("Operation " + str(ops) + "? ")
if op not in ops:
    print("-E- unknown operation: " + op)
    exit()


# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
# disable 'channel is already in use' warnings
GPIO.setwarnings(False)
# GPIO Map
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

#set all off
for r in relays:
    GPIO.output(int(r), GPIO.HIGH)


# if op == "on":
#     GPIO.output(int(relay), GPIO.LOW)
# else:
#     GPIO.output(int(relay), GPIO.HIGH)


print("relay " + relay + " is " + op)

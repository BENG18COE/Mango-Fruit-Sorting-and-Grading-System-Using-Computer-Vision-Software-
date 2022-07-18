

is_rasspberry_pi = False
try:
    import RPi.GPIO as GPIO
    from gpiozero import LoadAverage, DiskUsage
    is_rasspberry_pi = True
except ImportError:
    pass

import time
import subprocess
import re


BUZZER_PIN = 18


if is_rasspberry_pi:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)


def beep(duration=0.1):
    if is_rasspberry_pi:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)


def stop_beep():
    if is_rasspberry_pi:
        GPIO.output(BUZZER_PIN, GPIO.LOW)
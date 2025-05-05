import RPi.GPIO as GPIO
import time
from mqtt.client import publish
import config

LDR_PIN = 5

GPIO.setmode(GPIO.BCM)

def rc_time(pin):
    count = 0

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.1)

    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == GPIO.LOW:
        count += 1

    return count

def run():
    try:
        while True:
            value = rc_time(LDR_PIN)
            print(f"[LIGHT] LDR raw value: {value}")
            publish(config.TOPIC_LIGHT, value)
            time.sleep(config.INTERVAL_LIGHT)
    except KeyboardInterrupt:
        GPIO.cleanup()

import time
import RPi.GPIO as GPIO
from mqtt.client import publish
import config

TRIG = 26
ECHO = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150, 1)

    return distance

def run():
    try:
        while True:
            distance = measure_distance()
            print(f"[ALARM] Distance to alarm system: {distance} cm")
            publish(config.TOPIC_ALARM, distance)
            time.sleep(config.INTERVAL_ALARM)
    except KeyboardInterrupt:
        GPIO.cleanup()

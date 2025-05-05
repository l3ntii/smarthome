import time
import board
import busio
import adafruit_vl6180x
import config
from mqtt.client import publish

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

def run():
    while True:
        try:
            distance = sensor.range
            print(f"[SAFETY] Distance to motor: {distance} mm")
            publish(config.TOPIC_SAFETY, distance)
            time.sleep(config.INTERVAL_SAFETY)
        except Exception as e:
            print(f"[SAFETY] Sensor error: {e}")
            time.sleep(1)

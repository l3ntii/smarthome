import time
import board
import busio
import adafruit_hts221
from mqtt.client import publish
import config

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_hts221.HTS221(i2c)

def run():
    while True:
        temperature = round(sensor.temperature, 1)
        print(f"[TEMPERATURE] Temperature: {temperature} °C")
        publish(config.TOPIC_TEMPERATURE, temperature)
        time.sleep(config.INTERVAL_TEMPERATURE)

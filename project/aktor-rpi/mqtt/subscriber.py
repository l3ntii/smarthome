import paho.mqtt.client as mqtt
import config
from state import state

def on_connect(client, userdata, flags, rc):
    client.subscribe(config.TOPIC_TEMPERATURE)
    client.subscribe(config.TOPIC_LIGHT)
    client.subscribe(config.TOPIC_SAFETY)
    client.subscribe(config.TOPIC_ALARM)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    topic = msg.topic

    if topic == config.TOPIC_TEMPERATURE:
        state.temperature = float(payload)
    elif topic == config.TOPIC_LIGHT:
        state.light_value = int(payload)
    elif topic == config.TOPIC_SAFETY:
        state.motor_distance = int(payload)
    elif topic == config.TOPIC_ALARM:
        state.alarm_distance = float(payload)

def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)
    client.loop_start()
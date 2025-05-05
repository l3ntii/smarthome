import paho.mqtt.client as mqtt
import config

client = mqtt.Client()
client.connect(config.MQTT_BROKER, config.MQTT_PORT)

def publish(topic, value):
    payload = str(value)
    client.publish(topic, payload)

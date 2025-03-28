import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

MQTT_BROKER = "mosquitto"  
MQTT_PORT = 1883
MQTT_TOPIC = "challenge/dispositivo/rx"

def generate_message():
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": round(random.uniform(0, 1000), 2),
        "version": random.choice([1, 2])
    }

client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        mensaje = generate_message()
        client.publish(MQTT_TOPIC, json.dumps(mensaje))
        print(f"Publicado: {mensaje}")
        time.sleep(60) 
except KeyboardInterrupt:
    print("\nServicio detenido.")
    client.disconnect()

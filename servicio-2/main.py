import json
import time
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point

MQTT_BROKER = "mosquitto" 
MQTT_PORT = 1883
MQTT_TOPIC = "challenge/dispositivo/rx"

# Configuración de InfluxDB
INFLUX_URL = "http://influx:8086"  
INFLUX_ORG = "pruebainfluxdb"  
INFLUX_BUCKET = "system"
INFLUX_TOKEN = "admintesttoken"  


client_influx = InfluxDBClient(url=INFLUX_URL, org=INFLUX_ORG,
                           token=INFLUX_TOKEN)
write_api = client_influx.write_api()
print("Conectado a InfluxDB", write_api)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Mensaje recibido: {data}")

        point = (
            Point("dispositivos")
            .tag("version", str(data["version"]))  
            .field("time", data["time"])
            .field("value", float(data["value"]))  
        )

        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("Datos guardados")

    except Exception as e:
        print(f"Error: {e}")


client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message

for i in range(5):
    try:
        client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("✅ Conectado a MQTT")
        break
    except Exception as e:
        print(f"Intento {i+1}: No se pudo conectar a MQTT, reintentando en 5s...")
        time.sleep(5)

client_mqtt.subscribe(MQTT_TOPIC)
client_mqtt.loop_forever()

import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
client.connect("mosquitto", 1883, 60)
client.subscribe("challenge/dispositivo/rx")

print("Escuchando mensajes...")
client.loop_forever()

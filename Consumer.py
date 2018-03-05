import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
    else:
        print("Connectoion failed")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = mqtt.Client()
client.subscribe("alta/#")
client.subscribe("media/#")
client.subscribe("baja/#")
client.on_connect = on_connect
client.loop.start()
client.connect(host="172.24.42.93", port=8083, keepalive=60)

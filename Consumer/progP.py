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
client.on_message = on_message
client.connect("172.23.65.161", 8083,60)
client.loop_forever()

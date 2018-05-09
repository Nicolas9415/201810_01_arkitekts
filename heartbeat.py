import paho.mqtt.client as mq
import time


client = mq.Client("Py")
client.connect("192.168.43.148", 1883)

status=""

def on_message(client,usr,msg):
    global status
    print("health check")
    status=msg.payload

topic = "residencia.checks"
client.subscribe("security.sens")

def send():
    while True:
        time.sleep(10)
        client.publish(topic,"Todo bien")


def recive():
    badChecks=0
    while True:
        if "Hub ok" in status:
            client.publish("conjunto1/residencia1/heartbeathub", "todo bien")
            badChecks = 0
            time.sleep(10)

        else:
            badChecks=badChecks+1
            time.sleep(10)
        if badChecks > 4:
            client.publish("conjunto1/residencia1/propietario","CERRADURA FUERA DE LINEA")

client.on_message = on_message

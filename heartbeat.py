import paho.mqtt.client as paho
from datetime import datetime
import time
import threading

client = paho.Client("Py")
client.connect("192.168.43.148", 1883)
client.on_message=on_message

status=""

def on_message(client,usr,msg)
    status=msg.payload

topic = "residencia.checks"
client.subsribe("security.sens")

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
            badChecks=badchecks+1
            time.sleep(10)
        if badChecks >=5
            client.publish("conjunto1/residencia1/propietario","CERRADURA FUERA DE LINEA")

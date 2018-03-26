import paho.mqtt.client as mqtt
import time
import requests

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
    else:
        print("Connectoion failed")

def on_message(client, userdata, msg):
    print(msg.toic + " " + str(msg.qos) + " " + str(msg.payload))
    mail={
          'body':msg.payload.decode('utf-8'),
          'sbj':'msg.topic'
         }
    correo={"From: "+'servicio@yale.com'+"To: "+'residente@uniandes.edu.co'+"Subject: "+mail['sbj']+ "Body: "+ mail['body']}
    print(correo)
            
     


client = mqtt.Client()
client.subscribe("Apartamento1/residencia1/Alta/#")
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.23.65.161", puerto=8083)
client.loop_forever()

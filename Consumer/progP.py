import paho.mqtt.client as mqtt
import time
import requests

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected")
    else:
        print("Connectoion failed")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    mail={
          'body':userdata,
          'sbj':'alarm'
         }
    url='http://172.23.65.161/correo'
    correo={"From":+'servicio@yale.com'+"To: "+'residente@uniandes.edu.co'+"Subject: "+mail['sbj']+ "Body: "+'mail['body']}
    req= requests.post(url,correo)
            
     


client = mqtt.Client()
client.subscribe("Apartamento1/residencia1/Alta/#")
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.23.65.161", puerto=8083)
client.loop_forever()

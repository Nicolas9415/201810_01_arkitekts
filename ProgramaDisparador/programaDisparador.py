#!/usr/bin/env python
import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:8090')

def addPassword(val,index):
    if val<0 or val>9999:
        print("La clave debe contener como maximo 4 digitos")
    elif index<1 or index>20:
        print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
    else:
        producer.send('claves',"ADD_PASSWORD;"+str(val)+";"+str(index))

def updatePassword(val,index):
    if int(val)<0 or int(val)>9999:
        print("La clave debe contener como maximo 4 digitos")
    elif int(index)<1 or int(index)>20:
        print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
    else:
        producer.send('claves',"UPDATE_PASSWORD;"+str(val)+";"+str(index))
def deletePassword(index):
    if int(index)<1 or int(index)>20:
        print("El sistema solo puede almacenar 20 claves, y el indice debe ser mayor a 0")
    else:
        producer.send('claves',"DELETE_PASSWORD;"+str(index))
def deleteAllPasswords():
    producer.send('claves',"DELETE_ALL")

dicc={'add':addPassword,'update':updatePassword,'delP':deletePassword,'delAll':deleteAllPasswords}

command=input("Ingrese la operacion que desea relizar con los argumentos necesarios")
parts=command.split(";")

if len(parts)>2:
    dicc[parts[0]](parts[1],parts[2])
elif len(parts)==2:
    dicc[parts[0]](parts[1])
else:
    dicc[parts[0]]()











class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while not self.stop_event.is_set():
            producer.send('my-topic', b"test")
            producer.send('my-topic', b"\xc2Hola, mundo!")
            time.sleep(1)

        producer.close()


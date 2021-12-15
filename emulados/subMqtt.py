from paho.mqtt import client as mqtt_client
import time
from pymongo import MongoClient
import json    

# -- Configuração do mqtt -- 
broker = "localhost"
port = 1883
topic = "teste"
client_id = "guardiao_floresta_sub"

# -- Configuração do banco de dados --
cliente = MongoClient()
database = cliente.database_guardiao
collection = database.database_guardiao
guardiao_db = database.guardiao_db


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received: '{msg.payload.decode()}'")
        dado = json.loads(msg.payload.decode())
        print(type(dado))
        guardiao_db.insert_one(dado)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
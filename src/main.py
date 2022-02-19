import peewee
from guardiaoFloresta import  GuardiaoGas, GuardiaoTemp
from paho.mqtt import client as mqtt_client
import time
import json
from datetime import datetime

broker = "localhost"
port = 1883
topic = "teste"
client_id = "teste_sub"
global mensagem

dataDB_temp = {
            "Temperatura":"0",
            "Date":""
        }
dataDB_gas = {
		    "Gas":"0",
            "Date":""
        }
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
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        mensagem = ""
        mensagem = json.loads(msg.payload.decode())
        for key in mensagem:
            if key == "Temp":
                GuardiaoTemp.create(sensor_temp="temperature", value_temp=int(mensagem["Temp"]), join_date_temp=datetime.utcnow().isoformat())
                dataDB_temp["Temperatura"] = mensagem["Temp"]
                dataDB_temp["Date"] = datetime.utcnow().isoformat()
                print(dataDB_temp)

            elif key == "Gas":
                GuardiaoGas.create(sensor_gas="gas", value_gas=int(mensagem["Gas"]), join_date_gas=datetime.utcnow().isoformat())
                dataDB_gas["Gas"] = mensagem["Gas"]
                dataDB_gas["Date"] = datetime.utcnow().isoformat()
                print(dataDB_gas)


    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    #client.loop_start()
    client.loop_forever()

if __name__ == '__main__':
	try:
		GuardiaoTemp.create_table()
	except peewee.OperationalError:
		print('A Tabela de Temperatura existe')

	try:
		GuardiaoGas.create_table()
	except peewee.OperationalError:
		print("A Tabela de Gas existe")

	run()
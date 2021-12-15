from paho.mqtt import client as mqtt_client
from datetime import datetime
import time
import random
import json

broker = "localhost"
port = 1883
topic = "teste"
client_id = "guardiao_floresta_pub"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):

    while True:
        
        msg_collect = {
        "sensor": "MQ9",
        "guardiao_id": "1",
        "value": random.randint(0, 100),
        "date": datetime.now().isoformat(timespec='seconds')
        }

        result = client.publish(topic, json.dumps(msg_collect))
        status = result[0]
        
        if status == 0:
            print(f"Send '{msg_collect}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")
        
        time.sleep(5)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
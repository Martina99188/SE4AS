from db_storing import db_storing

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("indoor/#")
    client.subscribe("outdoor/#")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(str(msg.topic + " -> " + payload))
    db_storing.dbWrite(str(msg.topic), payload)

if __name__ == '__main__':

    client = mqtt.Client(client_id="client_id")
    #client.connect("localhost", 1883)
    client.connect("173.20.0.100", 1883)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
from random import randint
from paho.mqtt.client import Client


class Kitchen:
    @staticmethod
    def simulate(client: Client):

        light = randint(0, 5)
        temperature = randint(0, 5)
        humidity = randint(0, 5)
        movement = randint(0, 5)


        client.publish(f"windTurbine/{index}/speed", speed)
        client.publish(f"windTurbine/{index}/production", production)
        client.publish(f"windTurbine/{index}/vibration", vibration)
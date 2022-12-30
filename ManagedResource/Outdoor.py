from random import randint
from paho.mqtt.client import Client


class Outdoor:
    def simulate(client: Client):
        light = 0
        temperature = 0
        humidity = 0

    def __init__(self):
        self.light = 230
        self.temperature = 15
        self.humidity = 50


    def simulate(self, client: Client):
        self.light = self.light + randint(-1, 1)
        self.temperature = self.temperature + randint(-1, 1)
        self.humidity = self.humidity + randint(-1, 1)

        client.publish(f"outdoor/temperature", self.temperature)
        client.publish(f"outdoor/light", self.light)
        client.publish(f"outdoor/humidity", self.humidity)
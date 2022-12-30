from random import randint
from paho.mqtt.client import Client


class Room:

    roomName = ""
    light = 0
    temperature = 0
    humidity = 0
    movement = 0

    def __init__(self, roomName: str):
        self.roomName = roomName
        self.light = 180
        self.temperature = 20
        self.humidity = 30
        self.movement = 0


    def simulate(self, client: Client):
        self.light = self.light + randint(-1, 1)
        self.temperature = self.temperature # + randint(-1, 1)
        self.humidity = self.humidity + randint(-1, 1)
        self.movement = self.movement + randint(-1, 1)

        client.publish(f"indoor/{self.roomName}/light", self.light)
        client.publish(f"indoor/{self.roomName}/temperature", self.temperature)
        client.publish(f"indoor/{self.roomName}/humidity", self.humidity)
        client.publish(f"indoor/{self.roomName}/movement", self.movement)
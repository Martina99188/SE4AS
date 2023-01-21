import random
from random import randint
from paho.mqtt.client import Client
import Conditioner
import Lamp
import Dehumidifier
import Alarm
import AlarmActuator


class Room:

    roomName = ""
    light = 0
    temperature = 30
    humidity = 0
    movement = 1

    def __init__(self, roomName: str, light: int, temperature: int, humidity: int, movement: int):
        self.roomName = roomName
        self.light = light
        self.temperature = temperature
        self.humidity = humidity
        self.movement = movement
        self.alarm = Alarm.Alarm()
        self.actuators = [Conditioner.Conditioner(self),
                          Lamp.Lamp(self),
                          Dehumidifier.Dehumidifier(self),
                          AlarmActuator.AlarmActuator(self)]


    def simulate(self, client: Client):
        rand = random.randint(0,9)
        if rand == 0:
             self.light = self.light + randint(-1, 1)
             self.temperature = self.temperature + randint(-1, 1)
             self.humidity = self.humidity + randint(-1, 1)
        self.movement = randint(0,1)

        client.publish(f"indoor/{self.roomName}/light", self.light)
        client.publish(f"indoor/{self.roomName}/temperature", self.temperature)
        client.publish(f"indoor/{self.roomName}/humidity", self.humidity)
        client.publish(f"indoor/{self.roomName}/movement", self.movement)

        print(f'Publishing simulated data for room {self.roomName}')
from tenacity import retry

from Alarm import Alarm

from threading import Thread
import paho.mqtt.client as mqtt

class AlarmActuator:

    @retry()
    def __init__(self, room):
        self.room = room
        self.client = mqtt.Client(client_id=f"AlarmActuator_{room.roomName}")
        thread = Thread(target=self.initialize_mqtt)
        thread.start()

    def initialize_mqtt(self):
        self.client.connect("localhost", 1883)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        # print('Connesso')
        self.client.subscribe("alarm/#")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print("message received")
        topic = msg.topic
        topic_split = topic.split('/')
        room_name = topic_split[1]
        condition = topic_split[2]

        if room_name == self.room.roomName:
            if condition == 'activate':
                self.activeAlarm()
            else:
                self.disableAlarm()

    def activeAlarm(self):
        #  implement here listener from executor
        self.room.alarm.isActive = True

    def disableAlarm(self):
        #  implement here listener from executor
        self.room.alarm.isActive = False
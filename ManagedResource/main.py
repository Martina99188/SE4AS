import time
import paho.mqtt.client as mqtt
from Room import Room
from Outdoor import Outdoor
from Conditioner import Conditioner
from Dehumidifier import Dehumidifier
from Lamp import Lamp
from Alarm import Alarm
from AlarmActuator import AlarmActuator

def main():
    # MQTT client creation
    client = mqtt.Client("ManagedResource")
    client.on_publish = lambda client, userdata, mid: print("PUBLISH: ", mid)
    client.connect("localhost")
    #client.connect("172.17.0.2")

    # room creation
    living_room = Room(roomName="livingRoom")
    bath_room = Room(roomName="bathRoom")
    kitchen = Room(roomName="kitchen")
    outdoor = Outdoor()
    alarm = Alarm()

    # prova attuatori. DA RIMUOVERE una volta implementati i listener
    living_room.simulate(client=client)
    while True:
        Conditioner.increaseTemperature(room=living_room)
        if alarm.isActive==True:
            AlarmActuator.disableAlarm(alarm=alarm)
        else:
            AlarmActuator.activeAlarm(alarm=alarm)

        living_room.simulate(client=client)
        print("stato allarme: " + str(alarm.isActive))
        time.sleep(1)



    while True:
        # actuators listening
        """
        Conditioner.increaseTemperature(living_room)
        Conditioner.increaseTemperature(bath_room)
        Conditioner.increaseTemperature(kitchen)
        Conditioner.decreaseTemperature(living_room)
        Conditioner.decreaseTemperature(bath_room)
        Conditioner.decreaseTemperature(kitchen)
        Dehumidifier.increaseHumidity(living_room)
        Dehumidifier.increaseHumidity(bath_room)
        Dehumidifier.increaseHumidity(kitchen)
        Dehumidifier.decreaseHumidity(living_room)
        Dehumidifier.decreaseHumidity(bath_room)
        Dehumidifier.decreaseHumidity(kitchen)
        Lamp.increaseLight(living_room)
        Lamp.increaseLight(bath_room)
        Lamp.increaseLight(kitchen)
        Lamp.decreaseLight(living_room)
        Lamp.decreaseLight(bath_room)
        Lamp.decreaseLight(kitchen)
        
        living_room.simulate(client=client)
        bath_room.simulate(client=client)
        kitchen.simulate(client=client)
        outdoor.simulate(client=client)
        
        time.sleep(10)      
        """

if __name__ == "__main__":
    main()
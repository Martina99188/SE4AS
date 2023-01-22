import time
import paho.mqtt.client as mqtt
import tenacity
from Room import Room
from ModeDefinition import ModeDefinition

def main():
    # MQTT client creation
    client = mqtt.Client("ManagedResource", reconnect_on_failure=True)
    client.connect("localhost")

    # room creation
    rooms = []

    bath_room = Room(roomName="bathRoom",  light=140, temperature=22, humidity=50, movement=0)
    rooms.append(bath_room)
    kitchen = Room(roomName="kitchen", light=150, temperature=20, humidity=50, movement=0)
    rooms.append(kitchen)
    bedroom = Room(roomName="bedRoom",  light=140, temperature=22, humidity=50, movement=0)
    rooms.append(bedroom)
    living_room = Room(roomName="livingRoom", light=160, temperature=13, humidity=48, movement=0)
    rooms.append(living_room)

    # mode definition inside the knowledge and mode assignment to the rooms
    try:
        modes = ModeDefinition()
        modes.storeModes(rooms)
    except tenacity.RetryError as e:
        print("Max retries exceeded")


    while True:
        for room in rooms:
            room.simulate(client=client)

        time.sleep(1)

if __name__ == "__main__":
    main()
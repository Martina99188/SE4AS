import time
import paho.mqtt.client as mqtt
from Room import Room
from Outdoor import Outdoor

def main():
    client = mqtt.Client("ID1")
    client.on_publish = lambda client, userdata, mid: print("PUBLISH: ", mid)
    client.connect("localhost")

    living_room = Room(roomName="livingRoom")
    bath_room = Room(roomName="bathRoom")
    kitchen = Room(roomName="kitchen")
    outdoor = Outdoor()

    while True:
        living_room.simulate(client=client)
        bath_room.simulate(client=client)
        kitchen.simulate(client=client)
        #outdoor.simulate(client=client)

        time.sleep(10)


if __name__ == "__main__":
    main()

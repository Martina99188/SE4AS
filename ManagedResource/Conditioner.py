from Room import Room

class Conditioner:
    @staticmethod
    def increaseTemperature(room: Room):
        # implement here listener from executor
        room.temperature = room.temperature + 1

    @staticmethod
    def decreaseTemperature(room: Room):
        # implement here listener from executor
        room.temperature = room.temperature - 1
from Room import Room

class Dehumidifier:
    @staticmethod
    def increaseHumidity(room: Room):
        # implement here listener from executor
        room.humidity = room.humidity + 1

    @staticmethod
    def decreaseHumidity(room: Room):
        # implement here listener from executor
        room.humidity = room.humidity - 1
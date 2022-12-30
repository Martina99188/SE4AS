from Room import Room

class Lamp:
    @staticmethod
    def increaseLight(room: Room):
        #  implement here listener from executor
        room.light = room.light + 1

    @staticmethod
    def decreaseLight(room: Room):
        #  implement here listener from executor
        room.light = room.light - 1
import movementData
from lightData import LightData
from temperatureData import TemperatureData
from movementData import MovementData
from humidityData import HumidityData
from roomData import RoomData

def main():
    rooms = RoomData.getRoomsName()
    data = {}

    humidity_value = HumidityData.getHumidityDataFromDB('bathRoom')

    """
    for room in rooms:                
        # returns {time : value} of the humidity
        humidity_value = HumidityData.getHumidityDataFromDB(room)
        #
        data[room] = {'humidity': {humidity_value}}

        
        LightData.getLightDataFromDB(room)
        TemperatureData.getTemperatureDataFromDB(room)
        MovementData.getMovementDataFromDB(room)
    """

if __name__ == "__main__":
    main()
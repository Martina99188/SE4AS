import movementData
from lightData import LightData
from temperatureData import TemperatureData
from movementData import MovementData
from humidityData import HumidityData
from roomData import RoomData

def main():
    RoomData.getRoomsName()
    LightData.getLightDataFromDB()
    TemperatureData.getTemperatureDataFromDB()
    MovementData.getMovementDataFromDB()
    HumidityData.getHumidityDataFromDB()

if __name__ == "__main__":
    main()
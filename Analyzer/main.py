import movementData
import pprint
import numpy
from lightData import LightData
from temperatureData import TemperatureData
from movementData import MovementData
from humidityData import HumidityData
from roomData import RoomData

def main():
    rooms = RoomData.getRoomsName()
    data = {}

    #{room : {measurement : {time : value}}}
    for room in rooms:
        room_values = {}
        # returns {time : value} of the humidity
        humidity_value = HumidityData.getHumidityDataFromDB(room)
        room_values['humidity'] = humidity_value

        light_value = LightData.getLightDataFromDB(room)
        room_values['light'] = light_value

        temperature_value = TemperatureData.getTemperatureDataFromDB(room)
        room_values['temperature'] = temperature_value

        movement_value = MovementData.getMovementDataFromDB(room)
        room_values['movement'] = movement_value

        data[room] = room_values

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(data)
    check_trend(data)


def check_trend(data):
    for room in data:
        for measurement in data[room]:

            x = list(range(1,len(data[room][measurement]) + 1))

            y = data[room][measurement].values()

            # slope, intercept = numpy.polyfit(x,y,1)
            #
            # if slope > 0:
            #     print("Trend is increasing.")
            # elif slope < 0:
            #     print("Trend is decreasing.")
            # else:
            #     print("Trend is flat.")

            # y = [2, 4, 6, 8, 10]
            #
            # # calculate the slope of the line of best fit
            # slope, intercept = np.polyfit(x, y, 1)
            #
            # if slope > 0:
            #     print("Trend is increasing.")
            # elif slope < 0:
            #     print("Trend is decreasing.")
            # else:
            #     print("Trend is flat.")


if __name__ == "__main__":
    main()
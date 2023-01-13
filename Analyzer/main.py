import pprint
import numpy
import db_connector

def main():
    con = db_connector.DB_Connector()
    rooms = con.getRoomNames()
    measurements = con.getMeasurementsNames('indoor')
    data = {}

    #{room : {measurement : {time : value}}}
    for room in rooms:
        room_values = {}
        for measurement in measurements:
            # returns {time : value} of the measurement
            value = con.getDataFromDB(room, measurement)
            room_values[measurement] = value

        data[room] = room_values

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
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
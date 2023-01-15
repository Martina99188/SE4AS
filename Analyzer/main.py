import pprint
import numpy
import numpy as np
import db_connector

def main():
    con = db_connector.DB_Connector()
    rooms = con.getRoomNames()
    measurements = con.getMeasurementsNames('indoor')
    parameters_data = {}

    # dictionary of data are organized in this way {room : {measurement : {time : value}}}
    for room in rooms:
        room_values = {}
        for measurement in measurements:
            # returns {time : value} of the measurement
            value = con.getParametersDataFromDB(room, measurement)
            room_values[measurement] = value

        parameters_data[room] = room_values
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(data)
    check_parameters_symptoms(parameters_data)


    """
    check if our measured parameter are rising or falling
    trends = check_trend(data)
    print("i trend sono:")
    print(trends)

    presence = check_busy_time_slot(data)
    print("presenza persone in fasce orarie: ")
    print(presence)
    """

# calulate the mean of the last 5 minutes for each measured parameter (except the movement) and finds the symptoms
def check_parameters_symptoms(data):
    rooms = {}
    for room in data:
        values = {}
        for measurement in data[room]:
            if measurement != "movement":
                range = db_connector.DB_Connector.getRangeRoom(room = room)
                print(range)

                # al posto della media mettere stringa che dice se siamo sopra o sotto il range
                mean_parameter = numpy.mean(list(data[room][measurement].values()))
                values[measurement] = mean_parameter
        rooms[room] = values




def check_trend(data):
    trends = []
    for room in data:
        for measurement in data[room]:
            if measurement != "movement":
                x = list(range(1,len(data[room][measurement]) + 1))
                y = list(data[room][measurement].values())
                if len(y) < 3:
                    return None
                y = np.array(y)
                x = np.array(range(len(y)))
                A = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(A, y, rcond=None)[0]
                trend = 'constant'
                if m > 0:
                    trend = 'rising'
                if m < 0:
                    trend = 'falling'
                mean = np.mean(y)
                # return {'trend_rate': m, 'trend_offset': c, 'trend': trend, 'mean': mean}

                # organize data structure to return
                element = (room, measurement, trend)
                trends.append(element)
            else:
                continue
    #print(trends)
    return trends

def check_busy_time_slot(data):
    # TODO prendere media del movement per ogni quarto d'ora e vedere fasce orarie "affollate"
    presence = []
    for room in data:
        for measurement in data[room]:
            if measurement == "movement":
                #print(data[room][measurement])
                for element in data[room][measurement]:
                    # vedere come dividere i vari elementi per ogni quarto d'ora
                    #print(element)
                    continue
            else:
                continue
    # presence restituisce in base alla fascia orario la media di quanto è affollata una stanza ( 0 o 1 )
    return presence


if __name__ == "__main__":
    main()

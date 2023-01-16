import pprint
from datetime import datetime
from time import sleep

import numpy
import numpy as np
import db_connector
import requests

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


    symptoms = check_parameters_symptoms(parameters_data)
    url = 'http://173.20.0.105:5005/planner/symptoms'
    x = requests.post(url, json=symptoms)
    print(x.text)

    # blocco dedicato alla profilazione della presenza di persone in casa
    timeSlots = check_busy_time_slot()

    for timeSlot in timeSlots.items():
        db_connector.DB_Connector.storeTimeSlots(timeSlot)

# calulate the mean of the last 5 minutes for each measured parameter (except the movement) and finds the symptoms
def check_parameters_symptoms(data):
    rooms = {}
    for room in data:
        values = {}
        interval = db_connector.DB_Connector.getRangeRoom(room=room)
        for measurement in data[room]:
            if measurement != "movement":
                target = db_connector.DB_Connector.getTargetRoomParameter(measurement=measurement)
                mean_parameter = numpy.mean(list(data[room][measurement].values()))

                # 1 IF WE ARE OVER THE RANGE
                # 0 IF WE ARE INSIDE THE RANGE
                # -1 IF WE ARE UNDER THE RANGE
                if mean_parameter < target - interval:
                    values[measurement] = -1
                elif mean_parameter > target + interval:
                    values[measurement] = 1
                else:
                    values[measurement] = 0
        rooms[room] = values
    return rooms


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

def check_busy_time_slot():
    con = db_connector.DB_Connector()
    rooms = con.getRoomNames()
    datas = []
    for room in rooms:
        data = db_connector.DB_Connector.getPresenceDataFromDB(room)
        for element in data.items():
            datas.append(element)

    parsed_time = dict()
    for element in datas:
        time_string = element[0].split('T')
        time_string = time_string[1]
        time_string = time_string.split('.')
        time_string = time_string[0]

        date_obj = datetime.strptime(time_string, '%H:%M:%S')
        parsed_time[str(date_obj.time())] = element[1]

    fasce_orarie = dict()
    for hour in range(0, 24):
        for quarter in [('00', '14'), ('15', '29'), ('30', '44'), ('45', '59')]:
            parsed = list()
            for record in parsed_time.items():
                date_obj = datetime.strptime(record[0], '%H:%M:%S')
                if date_obj.hour == hour and (date_obj.minute > int(quarter[0]) and date_obj.minute < int(quarter[1])):
                    parsed.append(record[1])
                else:
                    parsed.append(0)
            mean = numpy.mean(parsed)
            if mean >= 0.5:
                fasce_orarie[f'{hour}:{quarter[0]} - {hour}:{quarter[1]}'] = 1
            else:
                fasce_orarie[f'{hour}:{quarter[0]} - {hour}:{quarter[1]}'] = 0
    return fasce_orarie

# TODO cambiare lo sleep con valore 300
if __name__ == "__main__":
    while True:
        main()
        sleep(20)

import pprint
from datetime import datetime
from time import sleep

import numpy
import numpy as np
import urllib3
from tenacity import retry, stop_after_attempt

import db_connector
import requests

@retry()
def main():
    try:
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
        url = 'http://localhost:5005/planner/symptoms'
        x = requests.post(url, json=symptoms)
    except Exception as exc:
        print(exc)

    # blocco dedicato alla profilazione della presenza di persone in casa
    timeSlots = check_busy_time_slot()

    for timeSlot in timeSlots.items():
        db_connector.DB_Connector.storeTimeSlots(timeSlot)


# calulate the mean of the last 5 minutes for each measured parameter (except the movement) and finds the symptoms
# @retry()
def check_parameters_symptoms(data):
    rooms = {}
    con = db_connector.DB_Connector()
    ranges = con.getAllRangesForModes()
    for room in data:
        values = {}
        interval = db_connector.DB_Connector.getRangeRoom(room=room)
        con = db_connector.DB_Connector()
        mode = con.getModeRoom(room)
        for measurement in data[room]:
            if measurement != "movement":
                target = db_connector.DB_Connector.getTargetRoomParameter(measurement=measurement)
                mean_parameter = numpy.mean(list(data[room][measurement].values()))
                #print(f'Measurement: {measurement}, Mean: {mean_parameter}, target: {target}, interval: {interval}')

                # 2 means to increase the value and set mode to danger
                # 1 means to increase the value
                # 0 don't do anything
                # -1 means to decrease the value
                # -2 means to decrease the value and set mode to danger

                # {
                #     danger: none
                #     danger: activate
                #     danger: deactivate
                # }
                print(f'\nMode: {mode}, Measurement: {measurement}, Value: {mean_parameter}, Target: {target}, Interval: {interval}, Danger Range: {ranges["danger"]}')
                if mode == 'eco' or mode == 'normal':
                    if mean_parameter > target + interval: #se misura è maggiore del range della mode attuale
                        if mean_parameter < target + int(ranges['danger']): #se misura è nel range della danger
                            values[measurement] = 1
                            print('No danger, simply decrease')
                        else:
                            if measurement == 'temperature':
                                values[measurement] = 2
                                print('Danger, decrease and set mode to danger')
                            else:
                                values[measurement] = 1
                                print('No danger, simply decrease')
                    elif mean_parameter < target - interval:  # se misura è minore del range della mode attuale
                        if mean_parameter > target - int(ranges['danger']):  # se misura è nel range della danger
                            values[measurement] = -1
                            print('No danger, simply increase')
                        else:
                            if measurement == 'temperature':
                                values[measurement] = -2
                                print('Danger, increase and set mode to danger')
                            else:
                                values[measurement] = -1
                                print('No danger, simply increase')
                elif mode == 'danger':
                    if measurement == "temperature":
                        print(f'\nMode: {mode}, Measurement: {measurement}, Target: {target}, Interval: {interval}, Danger Range: {ranges["danger"]}')
                        if mean_parameter > target + int(ranges['danger']): #se misura è superiore al range della danger
                            print('Danger active, simply decrease')
                            values[measurement] = 1
                        elif mean_parameter < target - int(ranges['danger']):  # se misura è superiore al range della danger
                            print('Danger active, simply increase')
                            values[measurement] = -1
                        elif mean_parameter < target + int(ranges['danger']) and measurement > target - int(ranges['danger']):
                            print('No more danger, deactivate alarm and set mode to eco')
                            values[measurement] = 3
                    else:
                        if mode == 'eco' or mode == 'normal':
                            if mean_parameter > target + interval:  # se misura è maggiore del range della mode attuale
                                if mean_parameter < target + int(
                                        ranges['danger']):  # se misura è nel range della danger
                                    values[measurement] = 1
                                    print('No danger, simply decrease')
                                else:
                                    if measurement == 'temperature':
                                        values[measurement] = 2
                                        print('Danger, decrease and set mode to danger')
                                    else:
                                        values[measurement] = 1
                                        print('No danger, simply decrease')
                            elif mean_parameter < target - interval:  # se misura è minore del range della mode attuale
                                if mean_parameter > target - int(
                                        ranges['danger']):  # se misura è nel range della danger
                                    values[measurement] = -1
                                    print('No danger, simply increase')
                                else:
                                    if measurement == 'temperature':
                                        values[measurement] = -2
                                        print('Danger, increase and set mode to danger')
                                    else:
                                        values[measurement] = -1
                                        print('No danger, simply increase')



                # # Se modalita è danger
                # #
                # #    Se parametro e' nel range normal
                # if mean_parameter < target - interval:
                #     if mode != 'danger':
                #         values[measurement] = -1
                #     else:
                #         values[measurement] = -2
                # elif mean_parameter > target + interval:
                #     if mode != 'danger':
                #         values[measurement] = 1
                #     else:
                #         values[measurement] = 2
                # else:
                #     values[measurement] = 0

        rooms[room] = values
    return rooms


@retry()
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

if __name__ == "__main__":
    while True:
        main()
        sleep(1)

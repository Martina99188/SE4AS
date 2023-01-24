import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from tenacity import retry

class DB_Connector:

    def __init__(self):

        self.org = "univaq"
        self.token = "seasinfluxdbtoken"
        #self.url = "http://173.20.0.102:8086/"
        self.url = "http://localhost:8086/"
        self.connect_to_influx()

    @retry()
    def connect_to_influx(self):
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)

    @retry()
    def getRoomNames(self) -> list:
        # influxdb connection
        query_api = self.client.query_api()
        query = f'import "influxdata/influxdb/schema" schema.tagValues(bucket: "seas", tag: "room")'
        results = query_api.query(org=self.org, query=query)

        # put the name of the rooms in a list
        rooms_name = []
        for element in results.to_values():
            rooms_name.append(list(element)[2])

        return rooms_name

    def getMeasurementsNames(self, zone: str) -> list:
        measurements = ["humidity","temperature","light"]
        return measurements

    @retry()
    def getParametersDataFromDB(self, room : str, measurement):
        query_api = self.client.query_api()
        query = f'from(bucket: "seas") |> range(start: -5m)  |> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  |> filter(fn: (r) => r["_field"] == "{measurement}")  ' \
                f'|> yield(name: "last")'
        result = query_api.query(org=self.org, query=query)

        values = {}
        for value in json.loads(result.to_json()):
            values[value['_time']] = value['_value']
        return values

    #@retry()
    def getPresenceDataFromDB(room: str):
        # influxdb connection
        org = "univaq"
        # token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas")  |> range(start: -7d)  ' \
                f'|> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  ' \
                f'|> filter(fn: (r) => r["_field"] == "movement")  |> yield(name: "mean")'
        result = query_api.query(org=org, query=query)
        values = {}
        for value in json.loads(result.to_json()):
            values[value['_time']] = value['_value']
        return values

    @retry()
    def getTargetRoomParameter(measurement : str):
        # influxdb connection
        org = "univaq"
        # token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas")  |> range(start: 2023-01-01T15:00:00Z)  ' \
                f'|> filter(fn: (r) => r["_measurement"] == "target")  ' \
                f'|> filter(fn: (r) => r["_field"] == "{measurement}")  ' \
                f'|> last(column: "_field")  |> yield(name: "last")'
        result = query_api.query(org=org, query=query)
        result = json.loads(result.to_json())[0]['_value']
        return result

    @retry()
    def getRangeRoom(room : str):
        # influxdb connection
        org = "univaq"
        # token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas")  |> range(start: 2023-01-01T15:00:00Z)  ' \
                f'|> filter(fn: (r) => r["_measurement"] == "indoor")  |> filter(fn: (r) => r["room"] == "{room}")  ' \
                f'|> filter(fn: (r) => r["_field"] == "range")  |> last(column: "_field")  ' \
                f'|> yield(name: "mean")'
        result = query_api.query(org=org, query=query)
        result = json.loads(result.to_json())[0]['_value']
        return result

    @retry()
    def getModeRoom(self, room : str):
        query_api = self.client.query_api()
        query = f'from(bucket: "seas") \
                |> range(start: 2023-01-01T15:00:00Z)\
                |> filter(fn: (r) => r["_measurement"] == "indoor")\
                |> filter(fn: (r) => r["room"] == "{room}")\
                |> filter(fn: (r) => r["_field"] == "mode")\
                |> last(column: "_field") \
                |> yield(name: "last")'
        result = query_api.query(org=self.org, query=query)
        parsed_result = json.loads(result.to_json())[0]['_value']
        return parsed_result

    # @retry()
    def getAllRangesForModes(self):
        query_api = self.client.query_api()
        query = f'from(bucket: "seas") \
                  |> range(start: 2023-01-01T15:00:00Z)\
                  |> filter(fn: (r) => r["_measurement"] == "mode")\
                  |> filter(fn: (r) => r["name"] == "danger" or r["name"] == "eco" or r["name"] == "normal")\
                  |> filter(fn: (r) => r["_field"] == "range")\
                  |> last(column: "_field")\
                  |> yield(name: "mean")'
        result = query_api.query(org=self.org, query=query)
        values = {}
        parsed = json.loads(result.to_json())
        # print(parsed)
        for obj in parsed:
            values[obj['name']] = obj['_value']

        return values
    @retry()
    def storeTimeSlots(timeSlot : tuple, room : str):
        # influxdb connection
        bucket = "seas"
        org = "univaq"
        token = "seasinfluxdbtoken"
        url = "http://localhost:8086/"
        #url = "http://173.20.0.102:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        measurement = "timeSlot"
        tag = room
        field = timeSlot[0]
        value = timeSlot[1]
        #print(f'Field: {field} - Value: {int(value)}')
        p = influxdb_client.Point(measurement).tag('room', tag).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

    #@retry()
    def get_room_time_slots(self, room : str, timeslot : str):
        query_api = self.client.query_api()
        query = f'from(bucket: "seas")  |> range(start: -7d)  ' \
                f'|> filter(fn: (r) => r["_measurement"] == "timeSlot")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  ' \
                f'|> filter(fn: (r) => r["_field"] == "{timeslot}")  ' \
                f'|> last(column: "_field")  |> yield(name: "mean")'
        result = query_api.query(org=self.org, query=query)
        parsed = json.loads(result.to_json())
        print(parsed[0]['_value'])
        #return parsed[0]['_value']
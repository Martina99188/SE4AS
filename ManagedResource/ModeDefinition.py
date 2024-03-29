import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from tenacity import *

class ModeDefinition:
    # method that stores the modes inside the knowledge (influxdb)
    @retry()
    def storeModes(self, rooms : list):
        # influxdb connection
        bucket = "seas"
        org = "univaq"
        token = "seasinfluxdbtoken"
        #url = "http://localhost:8086/"
        url = "http://173.20.0.102:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()

        # mode assignment to the rooms
        for room in rooms:
            measurement = "indoor"
            tag = room.roomName
            field = "mode"
            value = "normal"
            p = influxdb_client.Point(measurement).tag("room", tag).field(field, value)
            write_api.write(bucket=bucket, org=org, record=p)

            field = "range"
            value = 1
            p = influxdb_client.Point(measurement).tag("room", tag).field(field, value)
            write_api.write(bucket=bucket, org=org, record=p)
import influxdb_client
import urllib3
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import logging
from tenacity import *

class ModeDefinition:
    # method that stores the modes inside the knowledge (influxdb)
    @retry()
    def storeModes(self, rooms : list):
        # influxdb connection
        bucket = "seas"
        org = "univaq"
        token = "seasinfluxdbtoken"
        url = "http://localhost:8086/"
        #url = "http://173.20.0.102:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()

        # query = f'from(bucket: "seas") |> range(start: 2022-06-01T00:00:00Z)  ' \
        #         f'|> filter(fn: (r) => r["_measurement"] == "target")  ' \
        #         f'|> filter(fn: (r) => r["_field"] == "light" or r["_field"] == "temperature" or r["_field"] == "humidity")  ' \
        #         f'|> yield(name: "mean")'
        # query_exec = query_api.query(org=org, query=query)

        # DEFINITION OF TARGET VALUE INSIDE THE KNOWLEDGE

        # temperature target
        measurement = "target"
        field = "temperature"
        value = "20"
        p = influxdb_client.Point(measurement).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

        # light target
        measurement = "target"
        field = "light"
        value = "180"
        p = influxdb_client.Point(measurement).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

        # humidity target
        measurement = "target"
        field = "humidity"
        value = "50"
        p = influxdb_client.Point(measurement).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

        # DEFINITION OF THE MODES INSIDE THE KNOWLEDGE

        # query = 'from(bucket: "seas")  |> range(start: 2022-06-01T00:00:00Z)  ' \
        #         '|> filter(fn: (r) => r["_measurement"] == "mode")  |> filter(fn: (r) => r["_field"] == "range")  ' \
        #         '|> yield(name: "mean")'
        # query_exec = query_api.query(org=org, query=query)

        # eco-mode definition with range
        measurement = "mode"
        tag = "eco"
        field = "range"
        value = "5"
        p = influxdb_client.Point(measurement).tag("name", tag).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

        # normal-mode definition with range
        measurement = "mode"
        tag = "normal"
        field = "range"
        value = "1"
        p = influxdb_client.Point(measurement).tag("name", tag).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

        # danger-mode definition with range
        measurement = "mode"
        tag = "danger"
        field = "range"
        value = "15"
        p = influxdb_client.Point(measurement).tag("name", tag).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)

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
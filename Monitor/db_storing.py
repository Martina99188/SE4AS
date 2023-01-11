import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from datetime import datetime

class db_storing:
    @staticmethod
    def dbWrite(topic : str, value: int):
        #influxdb connection
        bucket = "seas"
        org = "univaq"
        token = "Zwf4BXDspYPSZJYreEw8yq5yccpw7i9an9vL-nF4cjZoTAY7MsCYzNI3yFaCCHy-rzzQr0mLZV-jsyeWJaopfg=="
        url = "http://173.20.0.102:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        #data formatting and storing
        topic = topic.split("/")
        measurement = topic[0]
        if measurement == 'indoor':
            field = topic[1] + "_" + topic[2]
        else:
            field = topic[1]
        p = influxdb_client.Point(measurement).field(field, int(value))
        write_api.write(bucket=bucket, org=org, record=p)


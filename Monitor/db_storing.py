from influxdb import InfluxDBClient
from datetime import datetime

class db_storing:
    @staticmethod
    def dbWrite():
        client = InfluxDBClient('localhost',8086,'admin','adminadmin','seas')
        print(str(client.get_list_database()))
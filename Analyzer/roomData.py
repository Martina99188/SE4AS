import influxdb_client

class RoomData:
    @staticmethod
    def getRoomsName():
        # influxdb connection
        org = "univaq"
        token = "seasinfluxdbtoken"
        # url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = 'import "influxdata/influxdb/schema" schema.tagValues(bucket: "seas", tag: "room")'
        results = query_api.query(org=org, query=query)

        rooms_name = []

        for element in results.to_values():
              print(rooms_name.append(element[3]))
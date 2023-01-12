import influxdb_client

class MovementData:
    @staticmethod
    def getMovementDataFromDB():
        # influxdb connection
        org = "univaq"
        token = "Zwf4BXDspYPSZJYreEw8yq5yccpw7i9an9vL-nF4cjZoTAY7MsCYzNI3yFaCCHy-rzzQr0mLZV-jsyeWJaopfg=="
        url = "http://173.20.0.102:8086/"
        # url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = 'from(bucket: "seas") |> range(start: 2021-01-01T00:00:00Z)' \
                '|> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                '|> filter(fn: (r) => r["_field"] == "bathRoom_movement")  ' \
                '|> yield(name: "mean")'
        query_exec = query_api.query(org=org, query=query)
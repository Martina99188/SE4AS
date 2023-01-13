import influxdb_client

class HumidityData:
    @staticmethod
    def getHumidityDataFromDB(room : str):
        # influxdb connection
        org = "univaq"
        token = "seasinfluxdbtoken"
        # url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas") |> range(start: -30m)  |> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  |> filter(fn: (r) => r["_field"] == "humidity")  ' \
                f'|> yield(name: "last")'
        result = query_api.query(org=org, query=query)

        print(result.to_json())



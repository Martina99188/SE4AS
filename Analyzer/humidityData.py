import influxdb_client
import json

class HumidityData:
    @staticmethod
    def getHumidityDataFromDB(room : str):
        # influxdb connection
        org = "univaq"
        token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        # url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas") |> range(start: -30m)  |> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  |> filter(fn: (r) => r["_field"] == "humidity")  ' \
                f'|> yield(name: "last")'
        result = query_api.query(org=org, query=query)
        #print(len(json.loads(result.to_json())))

        values = {}
        for value in json.loads(result.to_json()):
            values[value['_time']] = value['_value']

        return values



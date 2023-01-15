import pprint
import influxdb_client
import json

class DB_Connector:

    def getRoomNames(self) -> list:
        # influxdb connection
        org = "univaq"
        #token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'import "influxdata/influxdb/schema" schema.tagValues(bucket: "seas", tag: "room")'
        results = query_api.query(org=org, query=query)

        # put the name of the rooms in a list
        rooms_name = []
        for element in results.to_values():
            rooms_name.append(list(element)[2])

        return rooms_name


    def getMeasurementsNames(self, zone: str) -> list:
        """
        # influxdb connection
        org = "univaq"
        #token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'import "influxdata/influxdb/schema" \
                schema.measurementFieldKeys(bucket: "seas", measurement: "{zone}")'
        results = query_api.query(org=org, query=query)

        # put the name of the rooms in a list
        measurements_name = []
        for element in results.to_values():
            measurements_name.append(list(element)[2])
        """
        measurements = ["humidity","temperature","light"]
        return measurements

    def getParametersDataFromDB(self, room : str, measurement):
        # influxdb connection
        org = "univaq"
        #token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        #url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas") |> range(start: -5m)  |> filter(fn: (r) => r["_measurement"] == "indoor")  ' \
                f'|> filter(fn: (r) => r["room"] == "{room}")  |> filter(fn: (r) => r["_field"] == "{measurement}")  ' \
                f'|> yield(name: "last")'
        result = query_api.query(org=org, query=query)

        values = {}
        for value in json.loads(result.to_json()):
            values[value['_time']] = value['_value']

        return values


    # TODO mettere query fasce orarie generiche per il movimento dell'ultimo mese
    def getPresenceDataFromDB(self, room: str, measurement: str):
        pass


    def getTargetRoomParameter(self, room : str, measurement : str):
        pass

    def getRangeRoom(room : str):
        # influxdb connection
        org = "univaq"
        # token = "MBTON6j-f1cTTUVUOwu8BbP-AvsDpYBTJob6pxSkxFfKFnNYj_QqrlolasHOvOtxpXBAlgRAseNgvvxpZ5NAMA=="
        token = "seasinfluxdbtoken"
        # url = "http://173.20.0.102:8086/"
        url = "http://localhost:8086/"
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()
        query = f'from(bucket: "seas")  |> range(start: 2023-01-01T15:00:00Z)  ' \
                f'|> filter(fn: (r) => r["_measurement"] == "indoor")  |> filter(fn: (r) => r["room"] == "{room}")  ' \
                f'|> filter(fn: (r) => r["_field"] == "range")  |> yield(name: "last")'
        result = query_api.query(org=org, query=query)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(result.to_json())

        # TODO FARE QUERY PER PESCARA L'ULTIMO VALORE DI RANGE!!!!!!
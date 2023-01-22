import requests
from flask import Flask
from flask import jsonify
from flask import request
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

import ClientMQTT as mqtt

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
client = mqtt.MQTTClient(client_id = 'Executor')

@app.route("/<room>/<measurement>/<condition>")
def apply_tactic(room, measurement, condition):
    if measurement == 'temperature':
        client.publish(f'conditioner/{room}/{condition}', '')
    elif measurement == 'humidity':
        client.publish(f'dehumidifier/{room}/{condition}', '')
    else:
        client.publish(f'lamp/{room}/{condition}', '')

    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp

@app.route("/<room>/activate/alarm")
def trip_alarm(room):
    client.publish(f'alarm/{room}/activate', '')
    print('ALARM!')
    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp

@app.route("/mode/<room>/<mode>")
def change_mode(room, mode):
    print(room + " " + mode)
    bucket = "seas"
    org = "univaq"
    token = "seasinfluxdbtoken"
    url = "http://localhost:8086/"
    # url = "http://173.20.0.102:8086/"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    measurement = "indoor"
    tag = room
    field = "mode"
    value = mode
    p = influxdb_client.Point(measurement).tag("room", tag).field(field, value)
    write_api.write(bucket=bucket, org=org, record=p)
    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp


if __name__ == "__main__":

    app.run(debug=True, host='localhost', port=5006)
import requests
from flask import Flask
from flask import jsonify
from flask import request
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


if __name__ == "__main__":

    app.run(debug=True, host='localhost', port=5006)
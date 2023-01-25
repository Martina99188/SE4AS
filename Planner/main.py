import requests
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'

@app.route("/planner/symptoms", methods=["POST"])
def check_symptoms():
    symptoms = request.json
    url = 'http://173.20.0.106:5006'

    try:
        for room in symptoms:
            for measurement in symptoms[room]:
                print(f'\nRoom: {room}, Measurement: {measurement}, Condition: {symptoms[room][measurement]}')
                new_url = f'{url}/{room}/{measurement}'
                if symptoms[room][measurement] == 1:
                    x = requests.get(f'{new_url}/down')
                    print(f'{measurement} symptom: {symptoms[room][measurement]}. {measurement} should decrease.')
                elif symptoms[room][measurement] == -1:
                    x = requests.get(f'{new_url}/up')
                    print(f'{measurement} symptom: {symptoms[room][measurement]}. {measurement} should increase.')
                elif symptoms[room][measurement] == 2 :
                    alarm_url = f'{url}/{room}/activate/alarm'
                    x = requests.get(alarm_url)
                    print(f'{measurement} symptom: {symptoms[room][measurement]}. {measurement} should decrease. Alarm should be activated.')
                elif symptoms[room][measurement] == -2:
                    alarm_url = f'{url}/{room}/activate/alarm'
                    x = requests.get(alarm_url)
                    print(f'{measurement} symptom: {symptoms[room][measurement]}. {measurement} should increase. Alarm should be activated.')
                elif symptoms[room][measurement] == 3:
                    alarm_url = f'{url}/{room}/deactivate/alarm'
                    x = requests.get(alarm_url)
                    print(f'{measurement} symptom: {symptoms[room][measurement]}. Alarm should be deactivated.')
    except Exception as exc:
        print(exc)

    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp

@app.route("/planner/presence", methods=["POST"])
def change_mode():
    presence = request.json
    url = 'http://173.20.0.106:5006/mode'
    #1 means the room is in normal mode but should be eco-mode

    #0 means the room is in eco-mode but should be in normal mode

    for room in presence:
        if presence[room] == 1: #room is in normal mode but should be eco-mode
            x = requests.get(f'{url}/{room}/eco')
        if presence[room] == 2: #room is in eco-mode but should be in normal mode
            x = requests.get(f'{url}/{room}/normal')

    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    app.run(debug=True,host='173.20.0.105', port=5007)
import requests
from flask import Flask
from flask import jsonify
from flask import request
from tenacity import retry

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'

@app.route("/planner/symptoms", methods=["POST"])
def check_symptoms():
    # symptoms = '{"bathRoom": {"humidity": -1, "temperature": -1, "light": -1}, "kitchen": {"humidity": 0, "temperature": -1, "light": 1}, "livingRoom": {"humidity": -1, "temperature": -1, "light": 1}}'
    symptoms = request.json
    url = 'http://localhost:5006'

    try:
        for room in symptoms:
            for measurement in symptoms[room]:
                print(f'Room: {room}, Measurement: {measurement}, Condition: {symptoms[room][measurement]}')
                new_url = f'{url}/{room}/{measurement}'
                if symptoms[room][measurement] == 1:
                    x = requests.get(f'{new_url}/down')
                elif symptoms[room][measurement] == -1:
                    x = requests.get(f'{new_url}/up')
                elif symptoms[room][measurement] == 2 or measurement == -2:
                    alarm_url = f'{url}/{room}/activate/alarm'
                    x = requests.get(alarm_url)

    except Exception as exc:
        print(exc)

    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp

if __name__ == "__main__":
    app.run(debug=True,host='localhost', port=5005)
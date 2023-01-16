from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'

@app.route("/planner/symptoms", methods=["POST"])
def check_symptoms():
    # symptoms = '{"bathRoom": {"humidity": -1, "temperature": -1, "light": -1}, "kitchen": {"humidity": 0, "temperature": -1, "light": 1}, "livingRoom": {"humidity": -1, "temperature": -1, "light": 1}}'
    symptoms = request.json
    for room in symptoms:
        for measurement in symptoms[room]:
            if measurement == 1:
                print(symptoms[room][measurement])
            elif measurement == -1:
                print(symptoms[room][measurement])
            else:
                print(symptoms[room][measurement])

    resp = jsonify(success=True, error="none")
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True,host='173.20.0.105', port=5005)
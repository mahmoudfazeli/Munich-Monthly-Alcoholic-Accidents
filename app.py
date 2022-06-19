import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))


@app.route("/", methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    year = int(request.form.get('year')) - 2021
    month = int(request.form.get('month'))
    features = [[year, month]]
    prediction = int(model.predict(features)[0])

    return render_template(
        'index.html',
        prediction_text='prediction value is {}'.format(prediction))


@app.route("/api/predict", methods=["POST"])
def apiPredict():
    if "year" not in request.get_json() or "month" not in request.get_json():
        return {"Error": "Year ans Month are required!"}, 400

    data = request.get_json()
    year = data['year']
    month = data['month']

    if type(year) != int or month not in range(1, 13):
        return {"Error": "Year ans Month must be a valid numbers!"}, 400
    else:
        features = [[year - 2000, month]]
        prediction = int(model.predict(features)[0])
        return {'prediction': prediction}


if __name__ == "__main__":
    app.run(debug=True)
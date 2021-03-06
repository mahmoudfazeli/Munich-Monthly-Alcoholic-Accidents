import pandas as pd
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
    start_year = '2000'
    start_month = '1'
    end_year = str(request.form.get('year'))
    end_month = str(request.form.get('month'))
    id = (int(end_year)-int(start_year))*12+(int(end_month)-int(start_month))
    start_index = pd.to_datetime(start_year + start_month, format="%Y%m").to_period('M')
    end_index = pd.to_datetime(end_year + end_month, format="%Y%m").to_period('M')
    prediction = int(model.predict(start = start_index, end = end_index)[id])
    return render_template(
        'index.html',
        prediction_text='The predicted value of total alcoholic accidents on this month is: {}'.format(prediction))


@app.route("/api/predict", methods=["POST"])
def apiPredict():
    if "year" not in request.get_json() or "month" not in request.get_json():
        return {"Error": "Year and Month are required!"}, 400

    start_year = '2000'
    start_month = '1'
    data = request.get_json()
    end_year = data['year']
    end_month = data['month']

    if type(end_year) != int or end_month not in range(1, 13):
        return {"Error": "Please insert valid numbers!"}, 400
    else:
        end_year = str(end_year)
        end_month = str(end_month)
        id = (int(end_year)-int(start_year))*12+(int(end_month)-int(start_month))
        start_index = pd.to_datetime(start_year + start_month, format="%Y%m").to_period('M')
        end_index = pd.to_datetime(end_year + end_month, format="%Y%m").to_period('M')
        prediction = int(model.predict(start = start_index, end = end_index)[id])
        return {'prediction': prediction}


if __name__ == "__main__":
    app.run(debug=True)

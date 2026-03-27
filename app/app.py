# imports 
import joblib
from flask import Flask, request, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
model = joblib.load('model/xgb_gbr_stacked_model.pkl')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))
    new_data = (np.array(list(data.values())).reshape(1, -1))
    new_data[0, -1] = np.log(new_data[0, -1]) 
    output = model.predict(new_data)
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form

    new_data = np.array([
        int(data['area']),
        int(data['location']),
        int(data['bhk']),
        int(data['bath']),
        int(data['balcony']),
        int(data['parking']),
        int(data['furnishing']),
        int(data['property_type']),
        int(data['age'])
    ]).reshape(1, -1)
    print("INPUT:", new_data)

    output = model.predict(new_data)[0]

    return render_template(
        'home.html',
        prediction_text=f'The house price prediction is {output}'
    )

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True)

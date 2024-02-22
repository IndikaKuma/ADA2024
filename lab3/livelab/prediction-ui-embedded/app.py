# importing Flask and other modules
import json
import os

import pandas as pd
from flask import Flask, request, render_template, jsonify

from diabetes_predictor import DiabetesPredictor

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/checkdiabetes', methods=["GET", "POST"])
def check_diabetes():
    if request.method == "POST":
        prediction_input = [
            {
                "ntp": int(request.form.get("ntp")),  # getting input with name = ntp in HTML form
                "pgc": int(request.form.get("pgc")),  # getting input with name = pgc in HTML form
                "dbp": int(request.form.get("dbp")),
                "tsft": int(request.form.get("tsft")),
                "si": int(request.form.get("si")),
                "bmi": float(request.form.get("bmi")),
                "dpf": float(request.form.get("dpf")),
                "age": int(request.form.get("age"))
            }
        ]
        print(prediction_input)
        dp = DiabetesPredictor()
        df = pd.read_json(json.dumps(prediction_input), orient='records')
        status = dp.predict_single_record(df)
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(status[0])}), 200

    return render_template(
        "user_form.html")  # this method is called of HTTP method is GET, e.g., when browsing the link


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)

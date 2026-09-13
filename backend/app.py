
from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Initialize the Flask application
superkart_api = Flask("SuperKart Sales Predictor")

# Load the trained and serialized model
model = joblib.load("superkart_model.joblib")


@superkart_api.get("/")
def home():
    # Return a simple API status message.
    return jsonify({
        "message": "SuperKart Sales Prediction API is running"
    })


@superkart_api.get("/health")
def health():
    # Health-check endpoint used to verify that the API is running.
    return jsonify({
        "status": "healthy"
    })


@superkart_api.post("/v1/predict")
def predict_sales():
    # Return a sales prediction for one product-store record.
    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    try:
        input_data = pd.DataFrame([data])
        prediction = model.predict(input_data)[0]

        return jsonify({
            "prediction": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    # Return predictions for all rows in an uploaded CSV file.
    if "file" not in request.files:
        return jsonify({
            "error": "CSV file is required"
        }), 400

    try:
        file = request.files["file"]
        input_data = pd.read_csv(file)
        predictions = model.predict(input_data)

        output = {
            str(i): round(float(prediction), 2)
            for i, prediction in enumerate(predictions)
        }

        return jsonify(output)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


if __name__ == "__main__":
    superkart_api.run(
        host="0.0.0.0",
        port=7860
    )

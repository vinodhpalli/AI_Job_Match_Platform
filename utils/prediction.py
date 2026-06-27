import joblib
from tensorflow.keras.models import load_model

model = load_model("job_match_ann.keras")

scaler = joblib.load("scaler.pkl")


def predict(features):

    scaled = scaler.transform(features)

    prediction = model.predict(scaled, verbose=0)

    return float(prediction[0][0])
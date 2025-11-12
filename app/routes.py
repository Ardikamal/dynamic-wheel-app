# app/routes.py
import os
import pickle
from flask import Blueprint, render_template, request, jsonify, send_from_directory
import pandas as pd
import numpy as np

main_bp = Blueprint("main", __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model_rf.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dynamic_wheel_load.csv")

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, "rb") as f:
        payload = pickle.load(f)
    return payload  # dict with keys 'model' and 'features'

@main_bp.route("/")
def index():
    model_payload = load_model()
    has_model = model_payload is not None
    sample_head = None
    numeric_cols = []
    if os.path.exists(DATA_PATH):
        try:
            df = pd.read_csv(DATA_PATH)
            sample_head = df.head().to_dict(orient="records")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        except Exception:
            sample_head = None
    return render_template("index.html", has_model=has_model, sample_head=sample_head, numeric_cols=numeric_cols)

@main_bp.route("/predict", methods=["POST"])
def predict():
    payload = load_model()
    if payload is None:
        return jsonify({"error": "Model belum ada. Jalankan training terlebih dahulu."}), 400
    model = payload['model']
    features = payload['features']

    # dukung JSON body atau form data
    data = request.get_json() or request.form
    try:
        x = []
        for feat in features:
            if feat not in data:
                return jsonify({"error": f"Fitur '{feat}' tidak ditemukan di input."}), 400
            x.append(float(data[feat]))
        x_arr = np.array(x).reshape(1, -1)
        pred = model.predict(x_arr)[0]
        return jsonify({"predicted_wheel_load": float(pred)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/upload-dataset", methods=["POST"])
def upload_dataset():
    # menerima file CSV lewat form-data
    if 'file' not in request.files:
        return jsonify({"error": "Tidak ada file."}), 400
    f = request.files['file']
    save_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "dynamic_wheel_load.csv")
    f.save(save_path)
    return jsonify({"message": "Dataset berhasil diupload.", "path": save_path})

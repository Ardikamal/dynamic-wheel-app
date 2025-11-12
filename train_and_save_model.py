# train_and_save_model.py
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

DATA_PATH = os.path.join("data", "dynamic_wheel_load.csv")
MODEL_DIR = os.path.join("app", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model_rf.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

def load_data(path=DATA_PATH):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Dataset tidak ditemukan di: {path}. Letakkan file CSV di folder data/")
    df = pd.read_csv(path)
    print(f"[INFO] Loaded data shape = {df.shape}")
    return df

def prepare_xy(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) < 2:
        raise ValueError("Dataset harus berisi minimal 2 kolom numerik (fitur + target).")
    target_col = 'WheelLoad' if 'WheelLoad' in num_cols else num_cols[-1]
    feature_cols = [c for c in num_cols if c != target_col]
    df_clean = df[feature_cols + [target_col]].dropna()
    X = df_clean[feature_cols]
    y = df_clean[target_col]
    return X, y, feature_cols, target_col

def train_and_save(X, y, feature_cols):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"[INFO] Trained RF. Test MSE={mse:.4f}, R2={r2:.4f}")
    payload = {'model': rf, 'features': feature_cols}
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(payload, f)
    print(f"[INFO] Model saved to {MODEL_PATH}")

def main():
    try:
        df = load_data()
    except Exception as e:
        print("[ERROR]", e)
        return
    try:
        X, y, feature_cols, target_col = prepare_xy(df)
    except Exception as e:
        print("[ERROR]", e)
        return
    print(f"[INFO] Using target: {target_col}")
    print(f"[INFO] Feature columns: {feature_cols}")
    train_and_save(X, y, feature_cols)

if __name__ == "__main__":
    main()

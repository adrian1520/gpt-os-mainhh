# ADVANCED ML TRAINING (FEATURE ENGINEERING + XGBOOST)

import json
import os
import pickle
from xgboost import XGBClassifier

MEMORY_PATH = "memory/learning_log.json"
MODEL_PATH = "models/model_advanced.pkl"


def load_data():
    if not os.path.exists(MEMORY_PATH):
        return [], []

    with open(MEMORY_PATH, "r") as f:
        data = json.load(f)

    X, y = [], []

    for d in data:
        outcome = d.get("outcome")
        if outcome not in ["win", "loss"]:
            continue

        score = d.get("score", 50)
        risk = 1 if "high" in d.get("risk", "").lower() else 0

        # feature engineering
        confidence = score / 100
        risk_weighted = score * (1 - risk)

        X.append([score, risk, confidence, risk_weighted])

        y.append(1 if outcome == "win" else 0)

    return X, y


def train():
    X, y = load_data()

    if not X:
        print("No data")
        return

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Advanced model trained")


if __name__ == "__main__":
    train()

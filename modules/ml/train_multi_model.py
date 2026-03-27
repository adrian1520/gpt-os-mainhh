# MULTI-MODEL TRAINING + AUTO SELECTION

import json
import os
import pickle
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

MEMORY_PATH = "memory/learning_log.json"
MODEL_DIR = "models/"


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
        confidence = score / 100
        risk_weighted = score * (1 - risk)

        X.append([score, risk, confidence, risk_weighted])
        y.append(1 if outcome == "win" else 0)

    return X, y


def train_models(X, y):
    models = {}

    lr = LogisticRegression()
    lr.fit(X, y)
    models["logistic"] = lr

    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    xgb.fit(X, y)
    models["xgboost"] = xgb

    return models


def evaluate(models, X, y):
    scores = {}

    for name, model in models.items():
        preds = model.predict(X)
        acc = accuracy_score(y, preds)
        scores[name] = acc

    return scores


def select_best(models, scores):
    best_name = max(scores, key=scores.get)
    return best_name, models[best_name]


def save_model(name, model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"model_{name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)
    return path


def train():
    X, y = load_data()

    if not X:
        print("No data")
        return

    models = train_models(X, y)
    scores = evaluate(models, X, y)
    best_name, best_model = select_best(models, scores)

    path = save_model(best_name, best_model)

    print(f"Best model: {best_name}")
    print(f"Saved to: {path}")
    print(f"Scores: {scores}")


if __name__ == "__main__":
    train()

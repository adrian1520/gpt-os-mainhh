# TRAINING MODULE (ML)

import json
import os
from sklearn.linear_model import LogisticRegression
import pickle

MEMORY_PATH = "memory/learning_log.json"
MODEL_PATH = "models/model.pkl"


def load_data():
    if not os.path.exists(MEMORY_PATH):
        return [], []
    with open(MEMORY_PATH, "r") as f:
        data = json.load(f)

    X, y = [], []

    for d in data:
        score = d.get("score", 50)
        risk = 1 if "high" in d.get("risk","") else 0
        outcome = d.get("outcome")

        if outcome == "win":
            y.append(1)
        elif outcome == "loss":
            y.append(0)
        else:
            continue

        X.append([score, risk])

    return X, y


def train():
    X, y = load_data()

    if not X:
        print("No data")
        return

    model = LogisticRegression()
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print("Model trained")


if __name__ == "__main__":
    train()

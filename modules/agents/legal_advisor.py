import os, json

def main():
    if not os.path.exists("payload.json"):
        payload = {"status": "no_payload"}
    else:
        with open("payload.json") as f:
            payload = json.load(f)

    result = {
        "status": "processed",
        "input": payload
    }

    os.makedirs("events", exist_ok=True)
    with open("events/legal_result.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()

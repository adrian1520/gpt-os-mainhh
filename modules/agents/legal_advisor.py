import json

def main():
    with open("payload.json") as f:
        payload = json.load(f)

    result = {
        "status": "processed",
        "input": payload
    }

    with open("events/legal_result.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()

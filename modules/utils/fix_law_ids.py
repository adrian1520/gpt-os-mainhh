import json
import re

def fix_id(old_id):
    if not old_id:
        return old_id

    # KRO_1136 → KRO_113_6
    m = re.match(r'(KRO|KC|KPC)_(\d+?)(\d)$', old_id)
    if m:
        code, article, paragraph = m.groups()
        return f"{code}_{article}_{paragraph}"

    return old_id


def main():
    path = "knowledge/law/kro/kro.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    changed = False

    for item in data:
        old_id = item.get("id")
        new_id = fix_id(old_id)

        if old_id != new_id:
            print(f"{old_id} -> {new_id}")
            item["id"] = new_id
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("UPDATED")
    else:
        print("NO CHANGES")

if __name__ == "__main__":
    main()

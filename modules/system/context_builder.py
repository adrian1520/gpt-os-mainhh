import os, json, glob
from datetime import datetime

EVENTS_DIR = 'events/'
MEMORY_DIR = 'memory/'

def build_context():
    print("Rozpoczinam budowŅ kontekstu...")
    context_path = os.path.join(MEMORY_DIR, 'context_loader.json')
    
    context = {
        "current_mode": "GPT_OS",
        "active_case": "DEFAULT",
        "last_summary": "Inicjalizacja",
        "load_rules": { "always": ["memory/system_context.json"] }
    }
    if os.path.exists(context_path):
        with open(context_path, 'r', encoding='utf-8') as f:
            context = json.load(f)

    event_files = sorted(glob.glob(f"{EVENTS_DIR}/*.json"))
    recent_events = []
    
    for ef in event_files[-5:]:
        with open(ef, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                recent_events.append(f"[{os.path.basename(ef)}] {data.get('type', 'event')}: {data.get('summary', 'Brak')}")
            except Exception:
                pass

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context["last_summary"] = f"Aktualizacja: {now}\nOstatnie zdarzenia:\n" + "\n".join(recent_events)

    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(context_path, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
    print("Zaktualizowano context_loader.json")

if __name__ == "__main__":
    build_context()

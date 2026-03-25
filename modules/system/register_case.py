import os
import re
import shutil

def extract_signatura(text):
    match = re.search(r'[IVX]+ Nsm \d+/\d+', text)
    return match.group(0) if match else "UNKNOWN"

def sanitize(signatura):
    return signature.replace(" ", "_").replace("/", "_")

def main():
    input_dir = "Legal-os/Biuro_Podawcze"
    out_root = "Legal-os/Akta-Spraw"

    if not os.path.exists(input_dir):
        print("No Biuro_Podawcze directory - skip")
        return

    files = os.listdir(input_dir)
    if not files:
        print("No files in Biuro_Podawcze - skip")
        return

    for file in files:
        path = os.path.join(input_dir, file)
        if not os.path.isfile(path):
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        sig = extract_signature(text)
        if sig == "UNKNOWN": 
            print(f"Skip {file} - no signature")
            continue

        sig_clean = sanitize(sig)
        case_dir = os.path.join(out_root, sig_clean, "Pisma_Ori")
        os.makedirs(case_dir, exist_ok=True)

        out_path = os.path.join(case_dir, file.replace(".txt", ".md"))
        try:
            shutil.copy(path, out_path)
        except Exception as e:
            print(f"Error copying {file}: {e}")
            continue

        print(f"Registered: {file} -> {sig_clean}")

if __name__ == "__main__":
    main()
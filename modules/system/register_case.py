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

    for file in os.listdir(input_dir):
        path = os.path.join(input_dir, file)
        if not os.path.isfile(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        sig = extract_signature(text)
        sig_clean = sanitize(sig)

        case_dir = os.path.join(out_root, sig_clean, "Pisma_Ori")
        os.makedirs(case_dir, exist_ok=True)

        out_path = os.path.join(case_dir, file.replace(".txt", ".md"))
        shutil.copy(path, out_path)

        print(f"Registered: {file} -> {sig_clean}")

if __name__ == "__main__":
    main()
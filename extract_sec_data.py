import json
import os

# -----------------------------
# PATH CONFIGURATION
# -----------------------------

JSON_PATH = "data/sec_data/raw/2016q1.json"   # update if needed
OUTPUT_DIR = "data/sec_data/extracted_2019q1"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# LOAD JSON MANIFEST
# -----------------------------

with open(JSON_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print("Keys found in JSON:", manifest.keys())

# -----------------------------
# FILES TO EXTRACT
# -----------------------------

files_to_extract = {
    "num.txt": "num.txt",
    "pre.txt": "pre.txt",
    "sub.txt": "sub.txt",
    "readme.htm": "readme.htm",
    "tag.txt":"tag.txt"   # 👈 added for RAG context
}

# -----------------------------
# EXTRACT FILES
# -----------------------------

for json_key, output_filename in files_to_extract.items():
    if json_key not in manifest:
        print(f"⚠️ {json_key} not found in JSON — skipping")
        continue

    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(manifest[json_key])

    print(f"✅ Extracted {output_filename}")

print("\n🎉 SEC data extraction completed successfully.")
print("Files saved in:", OUTPUT_DIR)

import os
import time
import json
import re
import requests
from ddgs import DDGS

# =========================
# LOAD LABELS (SOURCE OF TRUTH)
# =========================
with open("model/labels.json", "r", encoding="utf-8") as f:
    raw_labels = json.load(f)

# convert {"0": "..."} → list
labels = list(raw_labels.values())

print(f"✅ TOTAL LABELS: {len(labels)}")

# =========================
# NORMALIZE LABEL → FILE NAME
# =========================
def normalize_label(text):
    text = text.lower()
    text = text.replace(" ", "_")

    # remove accents basic Vietnamese
    replacements = {
        "đ": "d",
        "ă": "a",
        "â": "a",
        "ê": "e",
        "ô": "o",
        "ơ": "o",
        "ư": "u",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r"[^\w_]", "", text)
    return text

# =========================
# BUILD IMAGE QUERIES AUTO (SYNC LABELS)
# =========================
image_queries = {
    label: label.replace("_", " ") + " món ăn Việt Nam"
    for label in labels
}

# =========================
# OUTPUT FOLDER
# =========================
os.makedirs("images", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# DOWNLOAD LOOP
# =========================
for dish, query in image_queries.items():

    filename = normalize_label(dish)
    path = f"images/{filename}.jpg"

    if os.path.exists(path):
        continue

    print(f"🔍 Searching: {query}")

    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=3)

            success = False

            for r in results:
                url = r.get("image")
                if not url:
                    continue

                try:
                    res = requests.get(url, headers=HEADERS, timeout=10)

                    if res.status_code != 200:
                        continue

                    if "image" not in res.headers.get("Content-Type", ""):
                        continue

                    with open(path, "wb") as f:
                        f.write(res.content)

                    print(f"✅ Saved: {filename}")
                    success = True
                    break

                except:
                    continue

            if not success:
                print(f"❌ Failed: {filename}")

        time.sleep(2)

    except Exception as e:
        print(f"⚠️ Error: {dish} -> {e}")

print("🎉 DONE ALL IMAGES")
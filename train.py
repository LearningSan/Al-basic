import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import json
import os

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("data/data.csv")

# =====================
# CLEAN TEXT
# =====================
df["ingredients"] = df["ingredients"].astype(str).str.lower().str.strip()

# =====================
# LABEL ENCODING
# =====================
labels = sorted(df["dish"].unique().tolist())
label2id = {l: i for i, l in enumerate(labels)}
id2label = {i: l for l, i in label2id.items()}

df["label"] = df["dish"].map(label2id)

# =====================
# SPLIT DATA
# =====================
X_train, X_val, y_train, y_val = train_test_split(
    df["ingredients"],
    df["label"],
    test_size=0.1,
    random_state=42,
    stratify=df["label"]
)

# =====================
# PIPELINE MODEL
# =====================
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        lowercase=True
    )),
    ("clf", LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    ))
])

# =====================
# TRAIN
# =====================
model.fit(X_train, y_train)

# =====================
# CREATE FOLDER
# =====================
os.makedirs("model", exist_ok=True)

# =====================
# SAVE MODEL (ONLY 1 FILE)
# =====================
joblib.dump(model, "model/model.pkl")

# =====================
# SAVE LABEL MAP
# =====================
with open("model/labels.json", "w", encoding="utf-8") as f:
    json.dump(id2label, f, ensure_ascii=False, indent=2)

print("✅ TRAIN DONE - PIPELINE READY (NO VECTOR PICKLE)")
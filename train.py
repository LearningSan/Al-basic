import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
import torch
import json
import os

# =====================
# DATA
# =====================
df = pd.read_csv("data/data.csv")

labels = sorted(df["dish"].unique().tolist())
label2id = {l: i for i, l in enumerate(labels)}
id2label = {i: l for l, i in label2id.items()}

df["label"] = df["dish"].map(label2id)

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["ingredients"],
    df["label"],
    test_size=0.1,
    random_state=42,
    shuffle=True
)

# =====================
# TOKENIZER
# =====================
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(texts):
    return tokenizer(list(texts), padding=True, truncation=True, max_length=64)

train_enc = tokenize(train_texts)
val_enc = tokenize(val_texts)

# =====================
# DATASET
# =====================
class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = list(labels)

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_enc, train_labels)
val_dataset = Dataset(val_enc, val_labels)

# =====================
# MODEL
# =====================
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(labels)
)

# =====================
# TRAINING ARGS (FIX FOR TRANSFORMERS 5.7)
# =====================
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=4,
    per_device_train_batch_size=8,

    eval_strategy="epoch",
    save_strategy="epoch",

    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

# =====================
# SAVE MODEL
# =====================
os.makedirs("model", exist_ok=True)

model.save_pretrained("model")
tokenizer.save_pretrained("model")

with open("model/labels.json", "w", encoding="utf-8") as f:
    json.dump(id2label, f, ensure_ascii=False)

print("✅ TRAIN DONE")
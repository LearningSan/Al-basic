from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import os
import re

app = FastAPI(title="🍳 AI Cooking API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# =========================
# GLOBAL STATE (lazy load)
# =========================
tokenizer = None
model = None
id2label = {}
recipes = {}

# =========================
# LOAD MODEL (LAZY)
# =========================
def load_model():
    global tokenizer, model, id2label, recipes

    if model is not None:
        return

    print("🚀 Loading model từ HuggingFace...")

    model_name = "OnlySan/AI-suggesting"

    token = os.getenv("HF_TOKEN")

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, token=token)

    model.eval()

    # load dữ liệu local
    with open(os.path.join(BASE_DIR, "model", "labels.json"), encoding="utf-8") as f:
        id2label = json.load(f)

    with open(os.path.join(BASE_DIR, "model", "recipes.json"), encoding="utf-8") as f:
        recipes = json.load(f)
# =========================
# STATIC FILES
# =========================
if os.path.exists(IMAGES_DIR):
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# =========================
# TEXT NORMALIZE
# =========================
def normalize(text: str):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    if len(text.split()) <= 2:
        text = "nguyên liệu món ăn: " + text

    return text

# =========================
# DISH LABELS
# =========================
dish_names = {
    "com_chien_trung": "Cơm chiên trứng",
    "trung_chien": "Trứng chiên",
    "bo_xao_hanh": "Bò xào hành",
    "mi_xao_trung": "Mì xào trứng",
    "mi_xao_bo": "Mì xào bò",
    "com_chien_duong_chau": "Cơm chiên Dương Châu",
    "trung_luoc": "Trứng luộc",
    "canh_trung_ca_chua": "Canh trứng cà chua",
    "trung_op_la": "Trứng ốp la",
    "bo_kho": "Bò kho",
    "thit_kho_trung": "Thịt kho trứng",
    "ga_chien": "Gà chiên",
    "ga_nuong": "Gà nướng",
    "sup_ga": "Súp gà",
    "com_ga": "Cơm gà",
    "bun_bo": "Bún bò",
    "pho_bo": "Phở bò",
    "mi_goi": "Mì gói",
    "trung_cuon": "Trứng cuộn",
    "trung_chien_ca_chua": "Trứng chiên cà chua",

    # thêm mới
    "com_chien_hai_san": "Cơm chiên hải sản",
    "tom_xao_toi": "Tôm xào tỏi",
    "ca_chien": "Cá chiên",
    "ca_kho": "Cá kho",
    "canh_rau": "Canh rau",
    "rau_xao_toi": "Rau xào tỏi",
    "dau_hu_chien": "Đậu hũ chiên",
    "dau_hu_sot_ca": "Đậu hũ sốt cà",
    "thit_xao_rau": "Thịt xào rau",
    "thit_nuong": "Thịt nướng",
    "trung_hap": "Trứng hấp",
    "canh_ga": "Canh gà",
    "mi_xao_hai_san": "Mì xào hải sản",
    "com_tam": "Cơm tấm",
    "suon_nuong": "Sườn nướng",
    "suon_kho": "Sườn kho",
    "lau_thai": "Lẩu Thái",
    "lau_ga": "Lẩu gà",
    "trung_xao_thit": "Trứng xào thịt",
    "trung_xao_hanh": "Trứng xào hành",
    "com_tron": "Cơm trộn",
    "mi_tron": "Mì trộn",
    "banh_mi_trung": "Bánh mì trứng",
    "banh_mi_thit": "Bánh mì thịt",
    "banh_mi_op_la": "Bánh mì ốp la"
}

# =========================
# INPUT MODEL
# =========================
class Input(BaseModel):
    ingredients: str

# =========================
# PREDICT
# =========================
def predict(text: str):
    load_model()

    if model is None:
        return [{"error": "Model chưa được load trên server"}]

    text = normalize(text)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=1)[0]
    topk = torch.topk(probs, k=3)

    results = []

    for i in range(len(topk.indices)):
        idx = int(topk.indices[i])
        confidence = topk.values[i].item()

        label = id2label[str(idx)]
        dish_key = label

        recipe = recipes.get(dish_key, {})

        img_path = os.path.join(IMAGES_DIR, f"{dish_key}.jpg")
        image_url = f"/images/{dish_key}.jpg" if os.path.exists(img_path) else "/images/default.jpg"

        results.append({
            "slug": dish_key,
            "dish": dish_names.get(dish_key, dish_key),
            "image": image_url,
            "confidence": round(confidence * 100, 2),
            "detail": recipe
        })

    return results

# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/predict")
def predict_api(data: Input):
    result = predict(data.ingredients)

    print("INPUT:", data.ingredients)
    print("OUTPUT:", result)

    return {
        "input": data.ingredients,
        "results": result
    }

@app.get("/dish/{dish_id}")
def get_dish_detail(dish_id: str):

    recipe = recipes.get(dish_id)

    if not recipe:
        dish_id_norm = dish_id.lower().strip()

        for k, v in recipes.items():
            if v.get("name", "").lower().strip() == dish_id_norm:
                recipe = v
                break

    if not recipe:
        return {
            "error": "Không tìm thấy món ăn",
            "dish_id": dish_id
        }

    return recipe
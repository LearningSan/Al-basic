from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse

import joblib
import json
import os
import re

# =========================
# APP
# =========================
app = FastAPI(title="🍳 AI Cooking API (LIGHT FIXED)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# =========================
# GLOBAL
# =========================
model = None
id2label = {}
recipes = {}

# =========================
# LABEL MAP (UI NAME)
# =========================
dish_names = {
    "com_chien_trung": "Cơm chiên trứng",
    "trung_chien": "Trứng chiên",
    "bo_xao_hanh": "Bò xào hành",
    "mi_xao_bo": "Mì xào bò",
    "canh_trung_ca_chua": "Canh trứng cà chua",
    "ga_chien": "Gà chiên",
    "ga_nuong": "Gà nướng",
    "com_ga": "Cơm gà",
    "bun_bo": "Bún bò",
    "pho_bo": "Phở bò",
    "mi_goi": "Mì gói",
    "ca_chien": "Cá chiên",
    "dau_hu_chien": "Đậu hũ chiên",
    "thit_xao_rau": "Thịt xào rau",
    "com_tron": "Cơm trộn"
}

# =========================
# LOAD MODEL (PIPELINE SKLEARN)
# =========================
def load_model():
    global model, id2label, recipes

    if model is not None:
        return

    print("🚀 Loading LIGHT MODEL...")

    model = joblib.load(os.path.join(BASE_DIR, "model/model.pkl"))

    # labels
    with open(os.path.join(BASE_DIR, "model/labels.json"), encoding="utf-8") as f:
        id2label = json.load(f)

    # recipes
    recipe_path = os.path.join(BASE_DIR, "model/recipes.json")
    if os.path.exists(recipe_path):
        with open(recipe_path, encoding="utf-8") as f:
            recipes = json.load(f)

    print("✅ MODEL LOADED")

# =========================
# STARTUP
# =========================
@app.on_event("startup")
def startup():
    load_model()

# =========================
# NORMALIZE TEXT
# =========================
def normalize(text: str):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

# =========================
# REQUEST MODEL
# =========================
class Input(BaseModel):
    ingredients: str

# =========================
# PREDICT
# =========================
def get_dish_name(slug):
    return recipes.get(slug, {}).get("name", slug)


def safe_recipe(label):
    return recipes.get(label, {
        "id": "-1",
        "name": label,
        "image": "/images/default.jpg",
        "ingredients": [],
        "steps": [],
        "ai_explain": "",
        "difficulty": "unknown",
        "cooking_time": 0
    })


def ingredient_match_score(text, ingredients):
    text_set = set(text.split())
    ing_set = set(ingredients)

    if not ing_set:
        return 0

    match = len(text_set & ing_set)
    return match / len(ing_set)


def predict(text: str):
    text = normalize(text)

    # 🔥 lấy score từ model nếu có
    try:
        scores = model.decision_function([text])[0]
    except:
        scores = [0] * len(id2label)

    results = []

    for idx, score in enumerate(scores):

        label = id2label.get(str(idx), str(idx))
        recipe = safe_recipe(label)

        ingredients = recipe.get("ingredients", [])
        ing_names = [i["name"] for i in ingredients]

        ing_score = ingredient_match_score(text, ing_names)

        # 🔥 hybrid scoring
        final_score = (float(score) * 0.7) + (ing_score * 0.3)

        results.append({
            "slug": label,
            "dish": recipe.get("name", label),
            "image": recipe.get("image", "/images/default.jpg"),
            "ingredients": ingredients,
            "steps": recipe.get("steps", []),
            "ai_explain": recipe.get("ai_explain", ""),
            "difficulty": recipe.get("difficulty", ""),
            "cooking_time": recipe.get("cooking_time", 0),
            "score": float(final_score),
            "match": float(ing_score)
        })

    # 🔥 sort + TOP 5
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:5]
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

# =========================
# GET RECIPE DETAIL
# =========================
@app.get("/dish/{dish_id}")
def get_dish_detail(dish_id: str):

    recipe = recipes.get(dish_id)

    if not recipe:
        # fallback theo id
        for k, v in recipes.items():
            if str(v.get("id")) == str(dish_id):
                recipe = v
                break

    if not recipe:
        return {
            "error": "Không tìm thấy món ăn",
            "dish_id": dish_id
        }

    return recipe

# =========================
# STATIC IMAGES
# =========================
if os.path.exists(IMAGES_DIR):
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
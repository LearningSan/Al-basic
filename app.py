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
app = FastAPI(title="🍳 AI Cooking API (AUTO FIXED)")

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
dish_names = {}

# =========================
# AUTO VIETNAMESE NAME MAP
# =========================
VN_DICT = {
    "com": "Cơm",
    "chien": "chiên",
    "xao": "xào",
    "kho": "kho",
    "nuong": "nướng",
    "hap": "hấp",
    "luoc": "luộc",
    "tron": "trộn",
    "canh": "canh",
    "bun": "bún",
    "pho": "phở",
    "mi": "mì",
    "ga": "gà",
    "bo": "bò",
    "ca": "cá",
    "trung": "trứng",
    "thit": "thịt",
    "tom": "tôm",
    "muc": "mực",
    "rau": "rau",
    "toi": "tỏi",
    "hanh": "hành",
    "ot": "ớt",
    "sa": "sả",
    "me": "me",
    "gung": "gừng",
    "kim_chi": "kim chi",
    "xuc_xich": "xúc xích",
    "pho_mai": "phô mai",
    "nuoc_mam": "nước mắm",
    "mat_ong": "mật ong",
    "chua_ngot": "chua ngọt",
    "bo_xao": "bò xào",
    "ga_xao": "gà xào",
    "ca_xao": "cá xào",
}

def auto_vietnamese_name(slug: str):
    parts = slug.split("_")
    words = []

    for p in parts:
        words.append(VN_DICT.get(p, p))

    return " ".join(words).capitalize()

# =========================
# LOAD MODEL
# =========================
def load_model():
    global model, id2label, recipes, dish_names

    if model is not None:
        return

    print("🚀 Loading MODEL...")

    model = joblib.load(os.path.join(BASE_DIR, "model/model.pkl"))

    with open(os.path.join(BASE_DIR, "model/labels.json"), encoding="utf-8") as f:
        id2label = json.load(f)

    recipe_path = os.path.join(BASE_DIR, "model/recipes.json")
    if os.path.exists(recipe_path):
        with open(recipe_path, encoding="utf-8") as f:
            recipes = json.load(f)

    # =========================
    # AUTO GENERATE dish_names
    # =========================
    for k in recipes.keys():
        dish_names[k] = auto_vietnamese_name(k)

    print(f"✅ Loaded {len(dish_names)} dish names")

# =========================
# STARTUP
# =========================
@app.on_event("startup")
def startup():
    load_model()

# =========================
# NORMALIZE
# =========================
def normalize(text: str):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

# =========================
# REQUEST
# =========================
class Input(BaseModel):
    ingredients: str

# =========================
# SAFE RECIPE
# =========================
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

# =========================
# SCORE
# =========================
def ingredient_match_score(text, ingredients):
    text_set = set(text.split())
    ing_set = set(ingredients)

    if not ing_set:
        return 0

    return len(text_set & ing_set) / len(ing_set)

# =========================
# PREDICT
# =========================
def predict(text: str):
    text = normalize(text)

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

        final_score = (float(score) * 0.7) + (ing_score * 0.3)

        results.append({
            "slug": label,
            "dish": dish_names.get(label, auto_vietnamese_name(label)),
            "image": recipe.get("image", "/images/default.jpg"),
            "ingredients": ingredients,
            "steps": recipe.get("steps", []),
            "ai_explain": recipe.get("ai_explain", ""),
            "difficulty": recipe.get("difficulty", ""),
            "cooking_time": recipe.get("cooking_time", 0),
            "score": float(final_score),
            "match": float(ing_score)
        })

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
# DETAIL
# =========================
@app.get("/dish/{dish_id}")
def get_dish_detail(dish_id: str):

    recipe = recipes.get(dish_id)

    if not recipe:
        for k, v in recipes.items():
            if str(v.get("id")) == str(dish_id):
                recipe = v
                break

    if not recipe:
        return {"error": "Không tìm thấy món ăn", "dish_id": dish_id}

    return recipe

# =========================
# STATIC
# =========================
if os.path.exists(IMAGES_DIR):
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LABEL_PATH = os.path.join(BASE_DIR, "model", "labels.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "model", "recipes.json")


# =========================
# CATEGORY MAP
# =========================
CATEGORY_MAP = {
    "com_": "rice",
    "mi_": "noodle",
    "pho_": "noodle",
    "bun_": "noodle",
    "bo_": "stir_fry",
    "ga_": "stir_fry",
    "ca_": "fried",
    "trung": "egg",
    "canh": "soup",
    "lau": "hotpot",
    "vit": "stew",
    "tom": "seafood",
    "muc": "seafood",
    "dau_hu": "vegetarian",
}


# =========================
# TAG MAP (mở rộng)
# =========================
TAG_MAP = {
    "com": ["rice", "quick"],
    "mi": ["noodle", "fast"],
    "bo": ["beef", "protein"],
    "ga": ["chicken", "protein"],
    "ca": ["fish", "protein"],
    "trung": ["egg", "protein"],
    "xao": ["stir_fry"],
    "chien": ["fried"],
    "nuong": ["grill"],
    "kho": ["stew"],
    "hap": ["healthy"],
}


# =========================
# INGREDIENT BASE
# =========================
INGREDIENT_BASE = {
    "bo": ["thịt bò", "tỏi", "nước mắm"],
    "ga": ["thịt gà", "muối", "tiêu"],
    "ca": ["cá", "muối", "gừng"],
    "trung": ["trứng", "muối"],
    "com": ["cơm"],
    "mi": ["mì"],
}


# =========================
# COOKING STYLE VARIANTS
# =========================
COOK_STYLES = {
    "xao": [
        "Xào nguyên liệu trên lửa lớn",
        "Thêm gia vị và đảo nhanh tay",
        "Giữ độ giòn tự nhiên"
    ],
    "chien": [
        "Làm nóng dầu ăn",
        "Chiên vàng đều hai mặt",
        "Vớt ra để ráo dầu"
    ],
    "nuong": [
        "Ướp gia vị 30 phút",
        "Nướng bằng than hoặc lò",
        "Trở đều để không cháy"
    ],
    "kho": [
        "Ướp gia vị đậm",
        "Kho nhỏ lửa đến khi sệt",
        "Thấm đều gia vị"
    ],
    "hap": [
        "Hấp cách thủy",
        "Giữ nguyên độ ngọt tự nhiên",
        "Không dùng nhiều dầu"
    ]
}


# =========================
# GENERAL STEPS (fallback)
# =========================
BASE_STEPS = [
    "Sơ chế nguyên liệu",
    "Chuẩn bị gia vị",
    "Chế biến món ăn",
    "Nêm nếm vừa ăn",
    "Trình bày món ăn"
]


# =========================
# TIPS VARIANTS
# =========================
TIPS = {
    "default": [
        "Nên ăn khi còn nóng",
        "Điều chỉnh gia vị theo khẩu vị"
    ],
    "fried": [
        "Chiên lửa vừa để không cháy",
        "Để ráo dầu trước khi ăn"
    ],
    "healthy": [
        "Hạn chế dầu mỡ",
        "Ăn kèm rau xanh"
    ],
    "stir_fry": [
        "Xào nhanh tay để giữ độ giòn",
        "Dùng lửa lớn"
    ]
}


# =========================
# NAME BEAUTIFY (giả có dấu)
# =========================
def pretty_name(slug):
    return slug.replace("_", " ").capitalize()


# =========================
# CATEGORY
# =========================
def detect_category(slug):
    for k, v in CATEGORY_MAP.items():
        if slug.startswith(k):
            return v
    return "auto"


# =========================
# TAGS
# =========================
def detect_tags(slug):
    tags = ["auto"]

    for k, v in TAG_MAP.items():
        if k in slug:
            tags += v

    return list(set(tags))


# =========================
# INGREDIENTS (đa dạng hơn)
# =========================
def detect_ingredients(slug):
    for k, base in INGREDIENT_BASE.items():
        if k in slug:
            return [
                {"name": ing, "amount": random.randint(50, 200), "unit": "g"}
                for ing in base
            ]

    return [{"name": "nguyên liệu", "amount": 1, "unit": "phần"}]


# =========================
# STEPS GENERATOR
# =========================
def detect_steps(slug):
    steps = []

    for k, style_steps in COOK_STYLES.items():
        if k in slug:
            steps += style_steps

    if not steps:
        steps = BASE_STEPS.copy()

    random.shuffle(steps)
    return steps


# =========================
# TIPS GENERATOR
# =========================
def detect_tips(category):
    tips = TIPS.get("default").copy()

    if category in TIPS:
        tips += TIPS[category]

    return list(set(tips))


# =========================
# MAIN
# =========================
with open(LABEL_PATH, "r", encoding="utf-8") as f:
    labels = json.load(f)

recipes = {}

for k, v in labels.items():

    slug = str(v)
    category = detect_category(slug)

    recipes[slug] = {
        "id": str(k),
        "name": pretty_name(slug),
        "image": f"/images/{slug}.jpg",
        "category": category,
        "tags": detect_tags(slug),

        "servings": random.randint(1, 3),
        "calories": random.randint(200, 800),

        "ingredients": detect_ingredients(slug),

        "steps": detect_steps(slug),

        "cooking_time": random.randint(5, 60),
        "difficulty": random.choice(["easy", "medium", "hard"]),

        "tips": detect_tips(category),

        "ai_explain": "Món ăn được AI tạo với nhiều phong cách nấu khác nhau để tăng đa dạng dữ liệu."
    }


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=2)

print("DONE recipes:", len(recipes))
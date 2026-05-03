import pandas as pd
import random

# =========================
# DISHES (GIỮ NHẸ + PHỔ BIẾN)
# =========================
dishes = {
    "com_chien_trung": ["cơm", "trứng"],
    "trung_chien": ["trứng"],
    "bo_xao_hanh": ["bò", "hành"],
    "mi_xao_bo": ["mì", "bò"],
    "canh_trung_ca_chua": ["trứng", "cà chua"],
    "ga_chien": ["gà"],
    "ga_nuong": ["gà"],
    "com_ga": ["cơm", "gà"],
    "bun_bo": ["bún", "bò"],
    "pho_bo": ["phở", "bò"],
    "mi_goi": ["mì"],
    "ca_chien": ["cá"],
    "dau_hu_chien": ["đậu hũ"],
    "thit_xao_rau": ["thịt", "rau"],
    "com_tron": ["cơm", "rau", "trứng"]
}

# =========================
# NATURAL HUMAN SPEECH (QUAN TRỌNG NHẤT)
# =========================
patterns = [
    # hỏi thật
    "mình có {ing} thì nấu gì được nhỉ",
    "tôi đang có {ing}, làm món gì đây",
    "có {ing} mà không biết nấu gì luôn",
    "giờ có {ing} thì ăn gì hợp lý",
    
    # sinh viên / nhanh
    "đói quá, có mỗi {ing} thôi thì làm gì ăn",
    "nhanh gọn với {ing} đi",
    "có {ing} ăn gì cho nhanh bây giờ",
    
    # gia đình
    "hôm nay nhà có {ing}, nấu món gì cho cả nhà",
    "tối nay có {ing}, ăn gì cho ngon đây",
    
    # casual chat
    "ê có {ing} nè, làm món gì ngon không",
    "không biết làm gì với {ing} luôn",
    
    # gợi ý
    "gợi ý món từ {ing} với",
    "từ {ing} thì nấu được món gì vậy",
]

# =========================
# CONTEXT REAL LIFE
# =========================
contexts = [
    "tối nay",
    "hôm nay",
    "giờ này",
    "bữa trưa",
    "bữa tối",
    "cuối tuần",
    "đi làm về",
    "ở nhà"
]

# =========================
# HUMAN EMOTION WORDS
# =========================
emotions = [
    "đói quá",
    "lười nấu luôn",
    "không biết ăn gì",
    "ngán cơm rồi",
    "muốn ăn gì đó ngon",
    "nhanh giúp mình với"
]

# =========================
# SLANG / NATURAL ENDINGS
# =========================
endings = [
    "được không?",
    "nhỉ?",
    "giờ sao ta",
    "gợi ý giúp mình với",
    "ăn gì hợp lý đây",
    "ngon không ta"
]

# =========================
# MAKE HUMAN SENTENCE
# =========================
def make_sentence(ingredients):
    ing = ", ".join(ingredients)

    base = random.choice(patterns).format(ing=ing)

    # thêm context (40%)
    if random.random() < 0.4:
        base = random.choice(contexts) + ", " + base

    # thêm cảm xúc (50%)
    if random.random() < 0.5:
        base = random.choice(emotions) + ", " + base

    # thêm ending tự nhiên (60%)
    if random.random() < 0.6:
        base += " " + random.choice(endings)

    return base

# =========================
# GENERATE DATASET
# =========================
data = []

TARGET_SIZE = 10000  # vừa đủ train tốt + không nặng

keys = list(dishes.keys())

for _ in range(TARGET_SIZE):
    dish = random.choice(keys)
    ingredients = dishes[dish].copy()

    random.shuffle(ingredients)

    # noise nhẹ kiểu người thật
    if random.random() < 0.2:
        ingredients.append(random.choice(["ngon", "nhanh", "đơn giản", "gia đình"]))

    text = make_sentence(ingredients)

    data.append([text, dish])

# =========================
# SAVE
# =========================
df = pd.DataFrame(data, columns=["ingredients", "dish"])
df.to_csv("data_human_like.csv", index=False, encoding="utf-8-sig")

print("✅ DONE: HUMAN-LIKE DATASET GENERATED")
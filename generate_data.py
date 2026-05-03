import pandas as pd
import random

# =========================
# DISHES
# =========================
dishes = {

# =========================
# 🍗 GÀ (30 món)
# =========================
"ga_chien": ["gà", "bột chiên", "dầu"],
"ga_ran": ["gà", "bột giòn", "dầu"],
"ga_nuong": ["gà", "muối", "tiêu", "than"],
"ga_nuong_muoi_ot": ["gà", "ớt", "muối", "mật ong"],
"ga_kho": ["gà", "nước mắm", "tiêu", "đường"],
"ga_kho_gung": ["gà", "gừng", "nước mắm"],
"ga_xao_sa_ot": ["gà", "sả", "ớt", "tỏi"],
"ga_hap_gung": ["gà", "gừng", "hành"],
"ga_hap_muoi": ["gà", "muối"],
"ga_ran_gion": ["gà", "bột giòn"],
"ga_quay": ["gà", "da giòn", "gia vị"],
"ga_xien_nuong": ["gà", "que xiên", "sốt"],
"ga_xao_nam": ["gà", "nấm", "tỏi"],
"ga_xao_rau": ["gà", "rau"],
"ga_xao_chua_ngot": ["gà", "dứa", "ớt"],
"ga_nuong_mat_ong": ["gà", "mật ong"],
"ga_ap_chao": ["gà", "bơ", "tỏi"],
"ga_chien_xu": ["gà", "bột xù"],
"ga_cuon": ["gà", "rau"],
"ga_sot_tieu_den": ["gà", "tiêu đen"],
"ga_rim": ["gà", "nước mắm"],
"ga_kho_tieu": ["gà", "tiêu"],
"ga_ham": ["gà", "thuốc bắc"],
"ga_xao_kim_chi": ["gà", "kim chi"],
"ga_xao_ot": ["gà", "ớt"],
"ga_nuong_la_chanh": ["gà", "lá chanh"],
"ga_chien_bo_toi": ["gà", "bơ", "tỏi"],
"ga_nuong_sate": ["gà", "sa tế"],
"ga_luoc": ["gà"],
"ga_nau_nuoc": ["gà", "nước dùng"],

# =========================
# 🥩 BÒ (30 món)
# =========================
"bo_xao_hanh": ["bò", "hành"],
"bo_xao_rau": ["bò", "rau"],
"bo_nuong": ["bò", "tiêu", "muối"],
"bo_kho": ["bò", "nước dừa", "quế"],
"bo_luc_lac": ["bò", "ớt chuông", "hành tây"],
"bo_ham": ["bò", "khoai tây"],
"bo_xao_nam": ["bò", "nấm"],
"bo_xao_toi": ["bò", "tỏi"],
"bo_xao_ot": ["bò", "ớt"],
"bo_nuong_sate": ["bò", "sa tế"],
"bo_chien": ["bò", "chiên"],
"bo_kho_tieu": ["bò", "tiêu"],
"bo_xao_kim_chi": ["bò", "kim chi"],
"bo_nuong_la_lot": ["bò", "lá lốt"],
"bo_nuong_muoi_ot": ["bò", "muối", "ớt"],
"bo_hap": ["bò", "hấp"],
"bo_xao_bap_cai": ["bò", "bắp cải"],
"bo_xao_sa": ["bò", "sả"],
"bo_rim": ["bò", "nước mắm"],
"bo_sot_nam": ["bò", "nấm"],
"bo_chien_gion": ["bò", "bột giòn"],
"bo_nuong_pho_mai": ["bò", "phô mai"],
"bo_xao_thai": ["bò", "rau thơm"],
"bo_xao_tieu_den": ["bò", "tiêu đen"],
"bo_kho_gung": ["bò", "gừng"],
"bo_xao_cai": ["bò", "cải"],
"bo_nuong_teriyaki": ["bò", "teriyaki"],
"bo_xao_ca_chua": ["bò", "cà chua"],
"bo_xao_bong_cai": ["bò", "bông cải"],
"bo_hap_tia_to": ["bò", "tía tô"],

# =========================
# 🐟 CÁ (30 món)
# =========================
"ca_chien": ["cá", "bột chiên"],
"ca_chien_xu": ["cá", "bột xù"],
"ca_kho": ["cá", "nước mắm"],
"ca_kho_to": ["cá", "nước dừa"],
"ca_hap": ["cá", "gừng"],
"ca_hap_xi_dau": ["cá", "xì dầu"],
"ca_nuong": ["cá", "muối", "ớt"],
"ca_nuong_muoi_ot": ["cá", "muối", "ớt"],
"ca_ran": ["cá"],
"ca_sot_ca": ["cá", "cà chua"],
"ca_kho_tieu": ["cá", "tiêu"],
"ca_hap_bia": ["cá", "bia"],
"ca_xien_nuong": ["cá"],
"ca_nuong_la_chanh": ["cá", "lá chanh"],
"ca_ngu_nuong": ["cá"],
"ca_dieu_hong": ["cá"],
"ca_basa_kho": ["cá"],
"ca_loc_nuong": ["cá"],
"ca_chien_gion": ["cá"],
"ca_kho_me": ["cá", "me"],
"ca_chien_sot": ["cá"],
"ca_hap_toi": ["cá", "tỏi"],
"ca_nuong_sa": ["cá", "sả"],
"ca_sot_me": ["cá", "me"],
"ca_nuong_hoa": ["cá"],
"ca_chien_muoi": ["cá"],
"ca_hap_nuoc": ["cá"],
"ca_rim": ["cá"],
"ca_kho_gung": ["cá", "gừng"],
"ca_nuong_tieu": ["cá", "tiêu"],

# =========================
# 🥚 TRỨNG (25 món)
# =========================
"trung_chien": ["trứng"],
"trung_op_la": ["trứng"],
"trung_luoc": ["trứng"],
"trung_hap": ["trứng"],
"trung_xao_thit": ["trứng", "thịt"],
"trung_chien_hanh": ["trứng", "hành"],
"trung_chien_thit": ["trứng", "thịt"],
"trung_chien_kim_chi": ["trứng", "kim chi"],
"trung_chien_toi": ["trứng", "tỏi"],
"trung_chien_pho_mai": ["trứng", "phô mai"],
"trung_cuon": ["trứng"],
"trung_chien_ca_chua": ["trứng", "cà chua"],
"trung_hap_thit": ["trứng", "thịt"],
"trung_chien_bo": ["trứng", "bò"],
"trung_chien_gion": ["trứng"],
"trung_rim": ["trứng"],
"trung_chien_nuoc_mam": ["trứng"],
"trung_chien_rau": ["trứng", "rau"],
"trung_chien_sot": ["trứng"],
"trung_kho": ["trứng"],
"trung_xao_hanh": ["trứng", "hành"],
"trung_chien_tom": ["trứng", "tôm"],
"trung_chien_nam": ["trứng", "nấm"],
"trung_hap_tom": ["trứng", "tôm"],
"trung_chien_xuc_xich": ["trứng", "xúc xích"],

# =========================
# 🍚 CƠM (25 món)
# =========================
"com_chien_trung": ["cơm", "trứng"],
"com_chien_thit": ["cơm", "thịt"],
"com_chien_ca": ["cơm", "cá"],
"com_chien_hai_san": ["cơm", "tôm", "mực"],
"com_chien_thap_cam": ["cơm"],
"com_ga": ["cơm", "gà"],
"com_suon": ["cơm", "sườn"],
"com_bi_cha": ["cơm"],
"com_tam": ["cơm", "sườn"],
"com_tron": ["cơm", "trứng"],
"com_rang_toi": ["cơm", "tỏi"],
"com_rang_dua_bo": ["cơm", "bò"],
"com_chay": ["cơm"],
"com_cari": ["cơm"],
"com_chien_ca_muoi": ["cơm", "cá"],
"com_chien_tom": ["cơm", "tôm"],
"com_chien_muc": ["cơm", "mực"],
"com_chien_xuc_xich": ["cơm", "xúc xích"],
"com_chien_nam": ["cơm", "nấm"],
"com_chien_ca_basa": ["cơm", "cá"],
"com_chien_bo": ["cơm", "bò"],
"com_chien_gung": ["cơm", "gừng"],
"com_chien_ot": ["cơm", "ớt"],
"com_chien_sate": ["cơm", "sa tế"],
"com_chien_dau": ["cơm", "đậu"],
"canh_chua_ca_loc": ["cá lóc", "me", "bạc hà", "cà chua"],
"canh_chua_tom": ["tôm", "me", "dứa"],
"canh_kim_chi": ["kim chi", "đậu hũ", "thịt"],
"canh_moc": ["giò sống", "nấm", "hành"],
"canh_cua": ["cua", "rau mồng tơi", "mướp"],
"canh_rieu_cua": ["cua", "cà chua", "đậu"],
"canh_bap_cai": ["bắp cải", "cà rốt", "thịt"],
"canh_suon_non": ["sườn", "cà rốt", "khoai tây"],
"canh_nam": ["nấm", "đậu hũ", "hành"],
"canh_ga_rau_cai": ["gà", "rau cải", "nấm"],
"canh_heo_tia_to": ["thịt heo", "tía tô"],
"canh_cai_bo_xoi": ["cải bó xôi", "tỏi"],
"canh_bi_do_thit": ["bí đỏ", "thịt bằm"],
"canh_khoai_mo": ["khoai mỡ", "tôm"],
"canh_mang": ["măng", "gà"],
"canh_chua_ca_chem": ["cá chẽm", "me", "rau"],
"canh_tom_rong_bien": ["tôm", "rong biển"],
"canh_rau_ngot": ["rau ngót", "thịt"],
"canh_suon_chua": ["sườn", "me"],
"canh_dau_hu_ca_chua": ["đậu hũ", "cà chua"],
"dau_hu_kim_chi": ["đậu hũ", "kim chi", "ớt"],
"dau_hu_ap_chao": ["đậu hũ", "bơ", "tỏi"],

"tom_chien": ["tôm", "bột chiên", "dầu"],
"tom_xao_toi": ["tôm", "tỏi", "bơ"],
"tom_nuong": ["tôm", "muối", "ớt"],

"muc_xao_sa_ot": ["mực", "sả", "ớt"],
"muc_chien": ["mực", "bột giòn"],
"muc_nuong": ["mực", "muối", "ớt"],

"vit_kho": ["vịt", "nước mắm", "gừng"],
"vit_nuong": ["vịt", "mật ong"],
"vit_luoc": ["vịt"],

"ech_xao_sa_ot": ["ếch", "sả", "ớt"],
"ech_chien": ["ếch", "bột giòn"],

"luon_xao": ["lươn", "sả", "ớt"],
"luon_kho": ["lươn", "tiêu"],

"cha_ca": ["chả cá", "thì là"],
"cha_gio": ["thịt", "bánh tráng"],
"nem_chua": ["thịt", "thính"],

"com_chien_dau_hu": ["cơm", "đậu hũ"],
"mi_xao_thap_cam": ["mì", "rau", "trứng", "thịt"],

"canh_mang_ga": ["măng", "gà"],
"lau_de": ["dê", "rau", "nước lẩu"]
}

if len(dishes) < 180:
    print("❌ CHƯA ĐỦ 180 MÓN:", len(dishes))
else:
    print("✅ ĐỦ 180 MÓN")
# =========================
# PATTERNS
# =========================
patterns = [
    "mình có {ing} thì nấu gì được nhỉ",
    "tôi đang có {ing}, làm món gì đây",
    "có {ing} mà không biết nấu gì luôn",
    "giờ có {ing} thì ăn gì hợp lý",
    "đói quá, có mỗi {ing} thôi thì làm gì ăn",
    "nhanh gọn với {ing} đi",
    "có {ing} ăn gì cho nhanh bây giờ",
    "hôm nay nhà có {ing}, nấu món gì cho cả nhà",
    "tối nay có {ing}, ăn gì cho ngon đây",
    "ê có {ing} nè, làm món gì ngon không",
    "không biết làm gì với {ing} luôn",
    "gợi ý món từ {ing} với",
    "từ {ing} thì nấu được món gì vậy"
]

# =========================
# CONTEXT / EMOTION / ENDINGS
# =========================
contexts = [
    "tối nay", "hôm nay", "giờ này",
    "bữa trưa", "bữa tối", "cuối tuần",
    "đi làm về", "ở nhà"
]

emotions = [
    "đói quá", "lười nấu luôn", "không biết ăn gì",
    "ngán cơm rồi", "muốn ăn gì đó ngon", "nhanh giúp mình với"
]

endings = [
    "được không?", "nhỉ?", "giờ sao ta",
    "gợi ý giúp mình với", "ăn gì hợp lý đây", "ngon không ta"
]

# =========================
# COOKING STYLE (bạn yêu cầu)
# =========================
cooking_styles = ["xào", "chiên", "luộc", "kho", "nướng", "trộn", "hấp"]

# =========================
# MAKE SENTENCE
# =========================
def make_sentence(ingredients):
    ing = ", ".join(ingredients)

    base = random.choice(patterns).format(ing=ing)

    # context
    if random.random() < 0.4:
        base = random.choice(contexts) + ", " + base

    # emotion
    if random.random() < 0.5:
        base = random.choice(emotions) + ", " + base

    # cooking style (NEW FEATURE)
    if random.random() < 0.3:
        base += " " + random.choice(cooking_styles)

    # ending
    if random.random() < 0.6:
        base += " " + random.choice(endings)

    return base


# =========================
# GENERATE DATASET
# =========================
data = []
TARGET_SIZE = 50000

keys = list(dishes.keys())

for _ in range(TARGET_SIZE):
    dish = random.choice(keys)
    ingredients = dishes[dish].copy()

    random.shuffle(ingredients)

    # noise nhẹ
    if random.random() < 0.2:
        ingredients.append(random.choice(["ngon", "nhanh", "đơn giản", "gia đình"]))

    text = make_sentence(ingredients)

    data.append([text, dish])

# =========================
# SAVE
# =========================
df = pd.DataFrame(data, columns=["ingredients", "dish"])
df.to_csv("data_human_like_20k.csv", index=False, encoding="utf-8-sig")

print("✅ DONE: 20K HUMAN-LIKE DATASET GENERATED")
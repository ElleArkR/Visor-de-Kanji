import requests
import json
import os

# JLPT N5 Kanji List (80 characters as provided in the prompt)
N5_KANJI_LIST = [
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万", "円", "時",
    "日", "週", "月", "年", "人", "女", "男", "子", "父", "母", "友", "先", "生", "学", "校",
    "高", "小", "中", "大", "長", "食", "見", "行", "来", "出", "入", "上", "下", "左", "右",
    "前", "後", "東", "西", "南", "北", "名", "語", "何", "私", "本", "読", "聞", "話", "買",
    "金", "土", "水", "火", "木", "今", "毎", "半", "午", "休", "気", "電", "車", "道", "駅",
    "社", "店", "銀", "病", "院", "花", "茶", "肉", "鳥", "魚", "空", "山", "川", "雨", "天"
]

# JLPT N4 Kanji List (ensure unique before combining)
N4_KANJI_ADDITIONS = [
    "悪", "安", "暗", "医", "意", "育", "員", "飲", "院", "運", "泳", "英", "駅", "園", "横", "屋", "温", "化", "荷", "界", "開",
    "階", "寒", "感", "漢", "館", "岸", "起", "期", "客", "究", "急", "球", "去", "橋", "業", "曲", "局", "銀", "区", "苦",
    "具", "君", "係", "軽", "血", "決", "研", "県", "庫", "湖", "向", "幸", "港", "号", "根", "祭", "皿", "仕", "死", "使",
    "始", "指", "歯", "詩", "次", "事", "持", "室", "社", "弱", "首", "秋", "週", "就", "拾", "宿", "主", "守", "取", "手",
    "酒", "受", "州", "集", "住", "重", "所", "暑", "助", "昭", "消", "商", "章", "勝", "乗", "植", "申", "身", "深", "進",
    "森", "整", "昔", "全", "相", "送", "想", "息", "速", "族", "他", "打", "対", "待", "代", "台", "第", "題", "炭", "短",
    "談", "着", "注", "柱", "帳", "調", "追", "定", "庭", "笛", "鉄", "転", "都", "度", "投", "豆", "島", "湯", "灯", "当",
    "答", "頭", "同", "道", "働", "特", "毒", "熱", "念", "波", "配", "倍", "箱", "畑", "発", "反", "坂", "板", "皮", "悲",
    "美", "鼻", "筆", "氷", "表", "秒", "病", "品", "負", "部", "服", "福", "物", "平", "返", "勉", "放", "味", "命", "面",
    "問", "役", "薬", "由", "油", "有", "遊", "予", "様", "洋", "陽", "葉", "踊", "流", "旅", "両", "緑", "礼", "列", "練",
    "路", "和"
]

# Combine N5 and N4 lists, ensuring uniqueness
# First, ensure N4_KANJI_ADDITIONS is unique (removes the duplicate "集" from the provided N4 list)
unique_n4_additions = sorted(list(set(N4_KANJI_ADDITIONS)))

# Then, combine with N5, ensuring overall uniqueness. N5 Kanji come first.
KANJI_LIST = N5_KANJI_LIST[:]  # Start with a copy of N5
for kanji in unique_n4_additions:
    if kanji not in KANJI_LIST:
        KANJI_LIST.append(kanji)

# Add sample Kanji for N3, N2, N1, ensuring uniqueness
N3_KANJI_SAMPLE = ["政", "議", "民", "連", "対", "選", "米", "果", "実", "府"]
N2_KANJI_SAMPLE = ["資", "際", "総", "設", "保", "派", "挙", "応", "検", "権"]
N1_KANJI_SAMPLE = ["麗", "鶴", "麓", "雅", "朕", "璽", "簿", "彰", "遡", "刹"] # Corrected list

HIGHER_LEVEL_SAMPLES = N3_KANJI_SAMPLE + N2_KANJI_SAMPLE + N1_KANJI_SAMPLE

for kanji in HIGHER_LEVEL_SAMPLES:
    if kanji not in KANJI_LIST:
        KANJI_LIST.append(kanji)

# print(f"Total unique Kanji in KANJI_LIST: {len(KANJI_LIST)}") # For debugging/verification

BASE_URL = "https://kanjiapi.dev/v1/kanji/"
OUTPUT_DIR = os.path.join("kanji_project", "data") # Ensure the base path is correct
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kanji_data.json") # Updated output filename

def fetch_kanji_data(kanji_char):
    """Fetches data for a single kanji character from KanjiAPI.dev."""
    url = f"{BASE_URL}{kanji_char}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {kanji_char}: {e}")
        return None

def main():
    """Main function to fetch data for all kanji and save it to a JSON file."""
    all_kanji_data = []
    processed_count = 0

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    for kanji_char in KANJI_LIST:
        print(f"Fetching data for {kanji_char}...")
        data = fetch_kanji_data(kanji_char)
        if data:
            # Extract required fields, handling missing ones with None
            extracted_data = {
                "kanji": data.get("kanji"),
                "grade": data.get("grade"),
                "stroke_count": data.get("stroke_count"),
                "meanings": data.get("meanings"),
                "kun_readings": data.get("kun_readings"),
                "on_readings": data.get("on_readings"),
                "jlpt": data.get("jlpt"),
                "unicode": data.get("unicode"),
            }
            all_kanji_data.append(extracted_data)
            processed_count += 1
        else:
            # Add a placeholder if fetching failed to maintain list integrity if needed,
            # or simply skip. For now, skipping.
            print(f"Skipping {kanji_char} due to previous error.")

    # Save the collected data to a JSON file
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_kanji_data, f, ensure_ascii=False, indent=4)
        print(f"\nSuccessfully processed {processed_count} kanji.")
        print(f"Data saved to {OUTPUT_FILE}")
    except IOError as e:
        print(f"Error writing data to file: {e}")

if __name__ == "__main__":
    main()

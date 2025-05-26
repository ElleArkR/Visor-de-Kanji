import requests
import json
import os

# JLPT N5 Kanji List (80 characters as provided in the prompt)
KANJI_LIST = [
    "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "百", "千", "万", "円", "時", 
    "日", "週", "月", "年", "人", "女", "男", "子", "父", "母", "友", "先", "生", "学", "校", 
    "高", "小", "中", "大", "長", "食", "見", "行", "来", "出", "入", "上", "下", "左", "右", 
    "前", "後", "東", "西", "南", "北", "名", "語", "何", "私", "本", "読", "聞", "話", "買", 
    "金", "土", "水", "火", "木", "今", "毎", "半", "午", "休", "気", "電", "車", "道", "駅", 
    "社", "店", "銀", "病", "院", "花", "茶", "肉", "鳥", "魚", "空", "山", "川", "雨", "天"
]
BASE_URL = "https://kanjiapi.dev/v1/kanji/"
OUTPUT_DIR = os.path.join("kanji_project", "data") # Ensure the base path is correct
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kanji_data_n5.json") # New output filename

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

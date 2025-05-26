import requests
import json
import os

KANJI_LIST = [
    '日', '月', '火', '水', '木', '金', '土', '一', '二', '三', '人', '女', '男', '子', '学', '生', '先', '何', '私', '本'
]
BASE_URL = "https://kanjiapi.dev/v1/kanji/"
OUTPUT_DIR = "kanji_project/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "kanji_data.json")

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

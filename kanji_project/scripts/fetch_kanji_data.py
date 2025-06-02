import requests
import json
import os
import time # Import time for adding delays

# KANJI_LIST will be populated from the API
KANJI_LIST = []

# print(f"Total unique Kanji in KANJI_LIST: {len(KANJI_LIST)}") # For debugging/verification

BASE_URL = "https://kanjiapi.dev/v1/kanji/"
ALL_KANJI_URL = "https://kanjiapi.dev/v1/kanji/all" # URL for fetching all kanji characters
WORDS_BASE_URL = "https://kanjiapi.dev/v1/words/" # URL for fetching example words
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

def fetch_example_words(kanji_char):
    """Fetches example words for a single kanji character from KanjiAPI.dev."""
    url = f"{WORDS_BASE_URL}{kanji_char}"
    print(f"Fetching example words for {kanji_char} from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # This will be a list of example words
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"No example words found for {kanji_char} (404 error).")
            return [] # Return empty list if no words found, common case
        else:
            print(f"HTTP error fetching example words for {kanji_char}: {e}")
            return [] # Return empty list on other HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching example words for {kanji_char}: {e}")
        return [] # Return empty list on other request errors
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for example words of {kanji_char}: {e}")
        return []

def fetch_all_kanji_list():
    """Fetches the list of all kanji characters from KanjiAPI.dev."""
    print(f"Fetching all kanji list from {ALL_KANJI_URL}...")
    try:
        response = requests.get(ALL_KANJI_URL)
        response.raise_for_status()
        kanji_list = response.json()
        print(f"Successfully fetched {len(kanji_list)} kanji characters.")
        return kanji_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all kanji list: {e}")
        return [] # Return empty list on error
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from all kanji list: {e}")
        return []

def main():
    """Main function to fetch data for all kanji and save it to a JSON file."""
    global KANJI_LIST # Declare KANJI_LIST as global to modify it
    all_kanji_data = []
    processed_count = 0
    fetch_delay = 0.1 # Small delay of 100ms between requests to be polite to the API

    # Fetch the full list of kanji characters first
    KANJI_LIST = fetch_all_kanji_list()

    if not KANJI_LIST:
        print("No kanji list fetched. Exiting.")
        return

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    for kanji_char in KANJI_LIST:
        print(f"Fetching data for {kanji_char}...")
        data = fetch_kanji_data(kanji_char)
        time.sleep(fetch_delay) # Add delay after kanji data fetch

        example_words = [] # Default to empty list
        if data and data.get("kanji"): # Proceed only if kanji data was fetched successfully
            # Fetch example words for the kanji
            # The API uses the kanji character itself in the URL for words
            example_words = fetch_example_words(data.get("kanji"))
            time.sleep(fetch_delay) # Add delay after example words fetch

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
                "example_words": example_words # Add the fetched example words
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

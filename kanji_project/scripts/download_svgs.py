import os
import json
import requests
import pathlib
import sys

# Define Paths and URLs
BASE_PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent
KANJI_DATA_JSON_PATH = BASE_PROJECT_DIR / 'data' / 'kanji_data.json' # Updated path
SVG_OUTPUT_DIR = BASE_PROJECT_DIR / 'data' / 'kanjivg_svgs'
KANJIVG_BASE_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/"

def download_all_svgs():
    """
    Downloads Kanji SVG files from KanjiVG based on data from kanji_data.json.
    """
    # Ensure output directory exists
    try:
        SVG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Ensured SVG output directory exists at: {SVG_OUTPUT_DIR}")
    except OSError as e:
        print(f"Error creating SVG output directory {SVG_OUTPUT_DIR}: {e}")
        sys.exit(1)

    # Load Kanji data
    if not KANJI_DATA_JSON_PATH.exists():
        print(f"Error: Kanji data file {KANJI_DATA_JSON_PATH} not found. Please run fetch_kanji_data.py first.")
        sys.exit(1)

    try:
        with open(KANJI_DATA_JSON_PATH, 'r', encoding='utf-8') as f:
            kanji_data_list = json.load(f)
        print(f"Successfully loaded Kanji data from {KANJI_DATA_JSON_PATH}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {KANJI_DATA_JSON_PATH}: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading Kanji data file {KANJI_DATA_JSON_PATH}: {e}")
        sys.exit(1)

    if not isinstance(kanji_data_list, list):
        print(f"Error: Kanji data in {KANJI_DATA_JSON_PATH} is not a list as expected.")
        sys.exit(1)

    # Initialize counters
    downloaded_count = 0
    skipped_count = 0
    error_count = 0
    not_found_count = 0

    print(f"\nStarting SVG download process. Total Kanji entries to process: {len(kanji_data_list)}")

    # Iterate and Download
    for index, kanji_entry in enumerate(kanji_data_list):
        if not isinstance(kanji_entry, dict):
            print(f"Warning: Entry at index {index} is not a dictionary. Skipping.")
            error_count +=1
            continue

        unicode_hex_value = kanji_entry.get('unicode')
        kanji_char = kanji_entry.get('kanji', 'N/A') # For logging

        if not unicode_hex_value or not isinstance(unicode_hex_value, str):
            print(f"Warning: Missing or invalid 'unicode' value for Kanji entry '{kanji_char}' (index {index}). Skipping.")
            error_count += 1
            continue

        # Format the SVG filename
        # The Unicode value is hex. Convert it to lowercase.
        # Ensure it's 5 digits, zero-padded (e.g., "04e00").
        # Append .svg (e.g., "04e00.svg").
        svg_filename = f"{unicode_hex_value.lower().zfill(5)}.svg"
        target_svg_path = SVG_OUTPUT_DIR / svg_filename
        download_url = KANJIVG_BASE_URL + svg_filename

        # Check if SVG already exists
        if target_svg_path.exists():
            # print(f"Skipping {svg_filename} for Kanji '{kanji_char}', already exists.")
            skipped_count += 1
            continue

        # Download
        print(f"Downloading {svg_filename} for Kanji '{kanji_char}' from {download_url}...")
        try:
            response = requests.get(download_url, timeout=10) # 10 second timeout
            if response.status_code == 200:
                with open(target_svg_path, 'wb') as f:
                    f.write(response.content)
                downloaded_count += 1
                # print(f"Successfully downloaded {svg_filename}")
            elif response.status_code == 404:
                print(f"Warning: SVG {svg_filename} for Kanji '{kanji_char}' not found at source (404). Skipping.")
                not_found_count += 1
            else:
                print(f"Error downloading {svg_filename} for Kanji '{kanji_char}': Status {response.status_code}. Skipping.")
                error_count += 1
        except requests.exceptions.Timeout:
            print(f"Error downloading {svg_filename} for Kanji '{kanji_char}': Request timed out. Skipping.")
            error_count += 1
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {svg_filename} for Kanji '{kanji_char}': {e}. Skipping.")
            error_count += 1
        except IOError as e:
            print(f"Error writing SVG file {target_svg_path} for Kanji '{kanji_char}': {e}. Skipping.")
            error_count +=1


    # Print Summary
    print("\n--- SVG Download Summary ---")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Skipped (already exist): {skipped_count}")
    print(f"Not found at source (404): {not_found_count}")
    print(f"Other errors: {error_count}")
    print(f"Total Kanji entries processed: {len(kanji_data_list)}")
    print("---------------------------\n")

if __name__ == "__main__":
    print("Starting Kanji SVG download script...")
    download_all_svgs()
    print("Kanji SVG download script finished.")

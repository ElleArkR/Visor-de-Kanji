import sqlite3
import json
import os
import pathlib

# Define Paths using pathlib for robustness
BASE_PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_PROJECT_DIR / "kanji.db"
JSON_DATA_PATH = BASE_PROJECT_DIR / "data" / "kanji_data.json"
TRANSLATIONS_PATH = BASE_PROJECT_DIR / "data" / "traducciones_es.json"
SVG_BASE_DIR_IN_STATIC = "svgs"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_schema(conn):
    """Ensures all necessary tables exist in the database."""
    cursor = conn.cursor()

    # Create 'kanjis' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kanjis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji_char TEXT UNIQUE NOT NULL,
        unicode TEXT UNIQUE NOT NULL,
        meanings TEXT,
        kun_readings TEXT,
        on_readings TEXT,
        stroke_count INTEGER,
        grade INTEGER,
        jlpt_level INTEGER,
        svg_filename TEXT
    )
    """)
    # print("Table 'kanjis' ensured to exist.")

    # Create 'example_words' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS example_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        reading TEXT NOT NULL,
        meaning_es TEXT NOT NULL,
        jlpt_level_word INTEGER,
        UNIQUE(word, reading, meaning_es)
    )
    """)
    # print("Table 'example_words' ensured to exist.")

    # Create 'kanji_example_word_assoc' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kanji_example_word_assoc (
        kanji_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        PRIMARY KEY (kanji_id, word_id),
        FOREIGN KEY (kanji_id) REFERENCES kanjis (id) ON DELETE CASCADE,
        FOREIGN KEY (word_id) REFERENCES example_words (id) ON DELETE CASCADE
    )
    """)
    # print("Table 'kanji_example_word_assoc' ensured to exist.")
    
    conn.commit()

def format_svg_filename(unicode_hex):
    """Formats the Unicode hex string to a 5-digit zero-padded SVG filename."""
    if unicode_hex:
        return f"{unicode_hex.lower().zfill(5)}.svg"
    return None

def list_to_comma_separated_string(data_list):
    """Converts a list of strings to a comma-separated string."""
    if data_list and isinstance(data_list, list):
        return ",".join(data_list)
    return None

def main():
    """Initializes the database, creates tables, and populates them with data."""
    if not JSON_DATA_PATH.exists():
        print(f"Error: JSON data file not found at {JSON_DATA_PATH}")
        print("Please run the fetch_kanji_data.py script first, or ensure the JSON file path is correct.")
        return

    conn = None
    kanjis_processed_count = 0
    example_words_processed_from_json = 0
    newly_inserted_example_words_count = 0
    associations_made_count = 0
    skipped_incomplete_json_examples = 0 # Counts JSON example word entries that couldn't be processed
    skipped_variant_data = 0 # Counts variants skipped due to missing word/reading/meaning
    
    try:
        conn = get_db_connection()
        ensure_schema(conn)

        with open(JSON_DATA_PATH, 'r', encoding='utf-8') as f:
            kanji_data_list = json.load(f)

        cursor = conn.cursor()
        print(f"Starting database population with {len(kanji_data_list)} kanji entries from JSON...")

        for kanji_entry in kanji_data_list:
            if not kanji_entry or not kanji_entry.get("kanji") or not kanji_entry.get("unicode"):
                continue
            
            kanji_char = kanji_entry.get("kanji")
            svg_filename = format_svg_filename(kanji_entry.get("unicode"))
            original_meanings_list = kanji_entry.get("meanings", [])
            meanings_to_store_str = list_to_comma_separated_string(original_meanings_list)
            kun_readings_str = list_to_comma_separated_string(kanji_entry.get("kun_readings"))
            on_readings_str = list_to_comma_separated_string(kanji_entry.get("on_readings"))
            grade = kanji_entry.get("grade")
            jlpt = kanji_entry.get("jlpt")

            current_kanji_id = None
            try:
                cursor.execute("""
                INSERT INTO kanjis (
                    kanji_char, unicode, meanings, kun_readings, on_readings, 
                    stroke_count, grade, jlpt_level, svg_filename
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(kanji_char) DO UPDATE SET
                    unicode=excluded.unicode,
                    meanings=excluded.meanings,
                    kun_readings=excluded.kun_readings,
                    on_readings=excluded.on_readings,
                    stroke_count=excluded.stroke_count,
                    grade=excluded.grade,
                    jlpt_level=excluded.jlpt_level,
                    svg_filename=excluded.svg_filename
                RETURNING id;
                """, (
                    kanji_char, kanji_entry.get("unicode"), meanings_to_store_str, 
                    kun_readings_str, on_readings_str, kanji_entry.get("stroke_count"),
                    grade, jlpt, svg_filename
                ))
                result = cursor.fetchone()
                if result:
                    current_kanji_id = result['id'] 
                    kanjis_processed_count +=1 
                else: 
                    cursor.execute("SELECT id FROM kanjis WHERE kanji_char = ?", (kanji_char,))
                    id_row = cursor.fetchone()
                    if id_row:
                        current_kanji_id = id_row['id']
                    else:
                        # print(f"CRITICAL: Kanji {kanji_char} was supposedly inserted/updated but ID could not be retrieved.")
                        pass # Soft fail for this kanji's examples
            except sqlite3.Error as e:
                # print(f"Error processing kanji {kanji_char}: {e}")
                continue 

            if not current_kanji_id:
                # print(f"Could not obtain ID for kanji {kanji_char}. Skipping example words.")
                continue

            json_example_words_list = kanji_entry.get("example_words", [])
            if isinstance(json_example_words_list, list):
                for ex_word_entry_from_json in json_example_words_list:
                    example_words_processed_from_json += 1
                    
                    meanings_list_for_word = ex_word_entry_from_json.get("meanings", [])
                    english_meaning_for_word = None
                    if meanings_list_for_word and isinstance(meanings_list_for_word, list) and \
                       len(meanings_list_for_word) > 0 and \
                       isinstance(meanings_list_for_word[0].get("glosses"), list) and \
                       len(meanings_list_for_word[0]["glosses"]) > 0:
                        english_meaning_for_word = meanings_list_for_word[0]["glosses"][0]
                    else:
                        # This example word entry in JSON lacks a usable English meaning
                        skipped_incomplete_json_examples +=1
                        continue # Skip this whole example word entry from JSON

                    variants_list = ex_word_entry_from_json.get("variants", [])
                    if not isinstance(variants_list, list) or not variants_list:
                        # This example word entry has no variants, or variants is not a list
                        skipped_incomplete_json_examples +=1 # Count it as skipped
                        continue # Skip this whole example word entry from JSON

                    for variant in variants_list:
                        written_word = variant.get("written")
                        pronounced_reading = variant.get("pronounced")
                        
                        if not all([written_word, pronounced_reading, english_meaning_for_word]):
                            skipped_variant_data += 1
                            continue 
                        
                        current_word_id = None
                        try:
                            cursor.execute("""
                            INSERT OR IGNORE INTO example_words (word, reading, meaning_es, jlpt_level_word) 
                            VALUES (?, ?, ?, ?)
                            """, (written_word, pronounced_reading, english_meaning_for_word, None))
                            
                            was_new_word_db_insertion = cursor.rowcount > 0
                            if was_new_word_db_insertion:
                                 newly_inserted_example_words_count +=1
                            
                            cursor.execute("SELECT id FROM example_words WHERE word = ? AND reading = ? AND meaning_es = ?", 
                                           (written_word, pronounced_reading, english_meaning_for_word))
                            word_id_row = cursor.fetchone()
                            if word_id_row:
                                current_word_id = word_id_row['id']
                            else:
                                continue
                        except sqlite3.Error as e:
                            continue 

                        if current_word_id and current_kanji_id:
                            try:
                                cursor.execute("INSERT OR IGNORE INTO kanji_example_word_assoc (kanji_id, word_id) VALUES (?, ?)", 
                                               (current_kanji_id, current_word_id))
                                if cursor.rowcount > 0:
                                    associations_made_count +=1
                            except sqlite3.Error as e:
                                pass 
            
        conn.commit()
        print(f"\nDatabase population complete.")
        print(f"Kanjis processed/updated in DB: {kanjis_processed_count}")
        print(f"Total example word entries (from JSON structure) processed: {example_words_processed_from_json}")
        print(f"Example word entries (from JSON) skipped due to no meanings/variants: {skipped_incomplete_json_examples}")
        print(f"Example word variants (within an entry) skipped due to missing data: {skipped_variant_data}")
        print(f"New unique example word variants actually inserted into DB: {newly_inserted_example_words_count}")
        print(f"New associations made between kanjis and word variants: {associations_made_count}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError: 
        print(f"Error: JSON data file not found at {JSON_DATA_PATH}.")
    except json.JSONDecodeError: 
        print(f"Error: Could not decode JSON from {JSON_DATA_PATH}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

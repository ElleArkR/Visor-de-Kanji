import sqlite3
import json
import os

DATABASE_PATH = os.path.join("kanji_project", "kanji.db")
JSON_DATA_PATH = os.path.join("kanji_project", "data", "kanji_data_n5.json") # Changed to N5 data file
SVG_BASE_DIR_IN_STATIC = "svgs" # This is relative to the static folder, if we decide to serve them

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
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
    print("Table 'kanjis' ensured to exist.")

    # Create 'example_words' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS example_words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        reading TEXT NOT NULL,
        meaning_es TEXT NOT NULL,
        jlpt_level_word INTEGER 
    )
    """)
    print("Table 'example_words' ensured to exist.")

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
    print("Table 'kanji_example_word_assoc' ensured to exist.")
    
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
    if not os.path.exists(JSON_DATA_PATH):
        print(f"Error: JSON data file not found at {JSON_DATA_PATH}")
        print("Please run the fetch_kanji_data.py script first, or ensure the JSON file path is correct.")
        return

    conn = None
    inserted_count = 0 # This count is for kanjis, will remain for now.
    try:
        conn = get_db_connection()
        ensure_schema(conn) # Call the updated schema function

        # The rest of the script populates the 'kanjis' table.
        # This part remains unchanged for this subtask.
        with open(JSON_DATA_PATH, 'r', encoding='utf-8') as f:
            kanji_data_list = json.load(f)

        cursor = conn.cursor()

        for kanji_data in kanji_data_list:
            if not kanji_data or not kanji_data.get("kanji") or not kanji_data.get("unicode"):
                print(f"Skipping invalid or incomplete record: {kanji_data}")
                continue

            svg_filename = format_svg_filename(kanji_data.get("unicode"))
            
            meanings_str = list_to_comma_separated_string(kanji_data.get("meanings"))
            kun_readings_str = list_to_comma_separated_string(kanji_data.get("kun_readings"))
            on_readings_str = list_to_comma_separated_string(kanji_data.get("on_readings"))

            # Handle potentially None numeric fields
            grade = kanji_data.get("grade")
            jlpt = kanji_data.get("jlpt")

            try:
                cursor.execute("""
                INSERT OR REPLACE INTO kanjis (
                    kanji_char, unicode, meanings, kun_readings, on_readings, 
                    stroke_count, grade, jlpt_level, svg_filename
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    kanji_data.get("kanji"),
                    kanji_data.get("unicode"),
                    meanings_str,
                    kun_readings_str,
                    on_readings_str,
                    kanji_data.get("stroke_count"),
                    grade, # grade can be None
                    jlpt,  # jlpt_level can be None
                    svg_filename
                ))
                if cursor.rowcount > 0:
                    inserted_count += 1
            except sqlite3.IntegrityError as e:
                print(f"Skipping duplicate kanji {kanji_data.get('kanji_char')} due to IntegrityError: {e}")
            except Exception as e:
                print(f"An error occurred while inserting {kanji_data.get('kanji_char')}: {e}")


        conn.commit()
        print(f"\nDatabase initialization complete.")
        print(f"{inserted_count} new records were inserted into the 'kanjis' table.")
        if inserted_count < len(kanji_data_list):
            print(f"{len(kanji_data_list) - inserted_count} records were already present or skipped due to errors.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except FileNotFoundError:
        print(f"Error: JSON data file not found at {JSON_DATA_PATH}")
        print("Please run the fetch_kanji_data.py script first.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_DATA_PATH}. File might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()

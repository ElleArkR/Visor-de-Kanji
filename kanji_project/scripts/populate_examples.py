import sqlite3
import json
import os

DATABASE_PATH = os.path.join("kanji_project", "kanji.db")

initial_example_data = [
    # Kanjis: 一
    { "word": "一つ", "reading": "ひとつ", "meaning_es": "Uno (general)", "jlpt_level_word": 5, "associated_kanji_chars": ["一"] },
    { "word": "一日", "reading": "ついたち", "meaning_es": "Primer día del mes", "jlpt_level_word": 5, "associated_kanji_chars": ["一", "日"] },
    { "word": "一番", "reading": "いちばん", "meaning_es": "El primero, número uno", "jlpt_level_word": 5, "associated_kanji_chars": ["一"] },
    # Kanjis: 日
    { "word": "今日", "reading": "きょう", "meaning_es": "Hoy", "jlpt_level_word": 5, "associated_kanji_chars": ["今", "日"] },
    { "word": "日曜日", "reading": "にちようび", "meaning_es": "Domingo", "jlpt_level_word": 5, "associated_kanji_chars": ["日"] },
    { "word": "日本", "reading": "にほん", "meaning_es": "Japón", "jlpt_level_word": 5, "associated_kanji_chars": ["日", "本"] },
    { "word": "毎日", "reading": "まいにち", "meaning_es": "Todos los días", "jlpt_level_word": 5, "associated_kanji_chars": ["毎", "日"] },
    # Kanjis: 人
    { "word": "一人", "reading": "ひとり", "meaning_es": "Una persona, solo", "jlpt_level_word": 5, "associated_kanji_chars": ["一", "人"] },
    { "word": "日本人", "reading": "にほんじん", "meaning_es": "Persona japonesa", "jlpt_level_word": 5, "associated_kanji_chars": ["日", "本", "人"] },
    { "word": "三人", "reading": "さんにん", "meaning_es": "Tres personas", "jlpt_level_word": 5, "associated_kanji_chars": ["三", "人"] },
    # Kanjis: 月
    { "word": "月曜日", "reading": "げつようび", "meaning_es": "Lunes", "jlpt_level_word": 5, "associated_kanji_chars": ["月"] },
    { "word": "一月", "reading": "いちがつ", "meaning_es": "Enero", "jlpt_level_word": 5, "associated_kanji_chars": ["一", "月"] },
    # Kanjis: 大
    { "word": "大学", "reading": "だいがく", "meaning_es": "Universidad", "jlpt_level_word": 5, "associated_kanji_chars": ["大", "学"] },
    { "word": "大きい", "reading": "おおきい", "meaning_es": "Grande", "jlpt_level_word": 5, "associated_kanji_chars": ["大"] },
]

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    # Correct path assuming script is in kanji_project/scripts/ and DB is in kanji_project/
    db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'kanji.db'))
    conn = sqlite3.connect(db_file_path)
    return conn

def main():
    conn = None
    words_attempted = 0
    words_inserted = 0
    assoc_attempted = 0
    assoc_inserted = 0
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for example in initial_example_data:
            words_attempted += 1
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO example_words (word, reading, meaning_es, jlpt_level_word)
                    VALUES (?, ?, ?, ?)
                """, (example["word"], example["reading"], example["meaning_es"], example.get("jlpt_level_word")))
                
                if cursor.rowcount > 0:
                    words_inserted += 1
                
                # Get the word_id (even if it was ignored, we need it for association)
                # If INSERT OR IGNORE and it was ignored, lastrowid is not updated reliably across all SQLite versions for this.
                # So, we query for the id.
                cursor.execute("SELECT id FROM example_words WHERE word = ? AND reading = ? AND meaning_es = ?", 
                               (example["word"], example["reading"], example["meaning_es"]))
                word_row = cursor.fetchone()
                if not word_row:
                    print(f"Aviso: No se pudo obtener el ID para la palabra '{example['word']}', omitiendo asociaciones.")
                    continue
                word_id = word_row[0]

                for kanji_char in example["associated_kanji_chars"]:
                    assoc_attempted += 1
                    cursor.execute("SELECT id FROM kanjis WHERE kanji_char = ?", (kanji_char,))
                    kanji_row = cursor.fetchone()
                    
                    if kanji_row:
                        kanji_id = kanji_row[0]
                        try:
                            cursor.execute("""
                                INSERT OR IGNORE INTO kanji_example_word_assoc (kanji_id, word_id)
                                VALUES (?, ?)
                            """, (kanji_id, word_id))
                            if cursor.rowcount > 0:
                                assoc_inserted += 1
                        except sqlite3.IntegrityError as e:
                             print(f"Aviso: Error de integridad al asociar kanji '{kanji_char}' con palabra '{example['word']}'. Puede que ya exista. Error: {e}")
                        except Exception as e_assoc:
                            print(f"Error inesperado al asociar kanji '{kanji_char}' con palabra '{example['word']}': {e_assoc}")
                    else:
                        print(f"Aviso: Kanji '{kanji_char}' no encontrado en la tabla 'kanjis'. No se creará asociación para la palabra '{example['word']}'.")
                        
            except sqlite3.IntegrityError as e:
                # This might happen if a unique constraint on example_words is violated (e.g. if we add one)
                print(f"Error de integridad al insertar palabra '{example['word']}'. Puede que ya exista o falte un campo NOT NULL. Error: {e}")
            except Exception as e_word:
                print(f"Error inesperado al procesar palabra '{example['word']}': {e_word}")


        conn.commit()
        print("\nPoblamiento de palabras de ejemplo completado.")
        print(f"Palabras procesadas: {words_attempted}")
        print(f"Palabras nuevas insertadas: {words_inserted}")
        print(f"Asociaciones intentadas: {assoc_attempted}")
        print(f"Asociaciones nuevas creadas: {assoc_inserted}")

    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    main()

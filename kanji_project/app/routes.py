from flask import Blueprint, jsonify, request, abort, render_template, current_app, send_from_directory
import os
from . import db # Assuming db.py is in the same directory (app)
from .translation_data import TRANSLATIONS_DICT # Import the dictionary
import json
from pathlib import Path

# Processed dictionary to ensure unique English keys, keeping the first encountered translation.
# _initial_translations = { ... } # This large dictionary is now removed

# The rest of the file remains the same, for example:
# bp = Blueprint('main', __name__)
# api_bp = Blueprint('api', __name__, url_prefix='/api')

# Example of how it might be used (conceptual, actual use will be in a translation function)
def get_translation_example(english_term):
    return TRANSLATIONS_DICT.get(english_term.lower(), english_term) # Return original if not found

# Actual route definitions and other logic follow...
# For example, the existing routes like:
# @main_bp.route('/')
# def index():
#     return render_template('index.html')

# Ensure all blueprints are defined
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

def get_example_words_for_kanji(kanji_id, conn):
    cursor = conn.cursor()
    query = """
    SELECT ew.word, ew.reading, ew.meaning_es 
    FROM example_words ew
    JOIN kanji_example_word_assoc kwa ON ew.id = kwa.word_id
    WHERE kwa.kanji_id = ?
    ORDER BY ew.word, ew.reading
    """
    cursor.execute(query, (kanji_id,))
    rows = cursor.fetchall()
    
    example_words_list = []
    if rows:
        for row_word_data in rows:
            english_meaning = row_word_data['meaning_es']
            
            translated_parts = []
            if english_meaning:
                for part in english_meaning.split('; '):
                    # Attempt to translate, fallback to original part if not in dict
                    translated_parts.append(TRANSLATIONS_DICT.get(part.strip().lower(), part.strip()))
            final_translated_meaning = '; '.join(translated_parts)

            example_words_list.append(
                f"{row_word_data['word']} ({row_word_data['reading']}): {final_translated_meaning}"
            )
    return example_words_list

def get_kanji_from_db(kanji_char):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    query = """ 
    SELECT 
        k.id as kanji_id, k.kanji_char, k.unicode, k.meanings, k.kun_readings, k.on_readings, 
        k.stroke_count, k.grade, k.jlpt_level, k.svg_filename
    FROM kanjis k
    WHERE k.kanji_char = ?
    """
    cursor.execute(query, (kanji_char,))
    row = cursor.fetchone()
    processed_row = _row_to_dict(row, conn) if row else None # Pass conn
    conn.close()
    return processed_row

def search_kanjis_in_db(query_term):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    like_query = f'%{query_term}%'
    
    query = """
    SELECT DISTINCT
        k.id as kanji_id, k.kanji_char, k.unicode, k.meanings, k.kun_readings, k.on_readings, 
        k.stroke_count, k.grade, k.jlpt_level, k.svg_filename
    FROM kanjis k
    LEFT JOIN kanji_example_word_assoc kwa ON k.id = kwa.kanji_id
    LEFT JOIN example_words ew ON kwa.word_id = ew.id
    WHERE k.kanji_char LIKE ? OR 
          k.meanings LIKE ? OR 
          k.kun_readings LIKE ? OR 
          k.on_readings LIKE ? OR
          ew.word LIKE ? OR 
          ew.meaning_es LIKE ? 
    LIMIT 20 
    """ 
    cursor.execute(query, (like_query, like_query, like_query, like_query, like_query, like_query))
    raw_rows = cursor.fetchall()
    
    results = []
    if raw_rows:
        for row in raw_rows:
            dict_row = _row_to_dict(row, conn) # Pass conn
            if dict_row:
                results.append(dict_row)
    conn.close()
    return results

# Helper functions (simplified)
def _comma_separated_to_list(comma_str):
    return [s.strip() for s in comma_str.split(',') if s.strip()] if comma_str else []

def _row_to_dict(row, conn): # Added conn parameter
    if not row:
        return None
    
    # Ensure that 'row' is a dictionary-like object (e.g., sqlite3.Row)
    # If it's just a tuple, this direct conversion might not work as expected for dict(row)
    # However, db.get_db_connection() sets conn.row_factory = sqlite3.Row, so it should be fine.
    base_dict = dict(row) 
    
    english_meanings_str = base_dict.get('meanings')
    english_meanings_list = _comma_separated_to_list(english_meanings_str)
    translated_meanings_kanji = []
    if english_meanings_list:
        for meaning in english_meanings_list:
            translated_meanings_kanji.append(TRANSLATIONS_DICT.get(meaning.lower(), meaning))
    
    kanji_data = {
        'kanji_id': base_dict.get('kanji_id'),
        'kanji_char': base_dict.get('kanji_char'),
        'unicode': base_dict.get('unicode'),
        'stroke_count': base_dict.get('stroke_count'),
        'grade': base_dict.get('grade'),
        'jlpt_level': base_dict.get('jlpt_level'),
        'svg_filename': base_dict.get('svg_filename'),
        'meanings': translated_meanings_kanji,
        'kun_readings': _comma_separated_to_list(base_dict.get('kun_readings')),
        'on_readings': _comma_separated_to_list(base_dict.get('on_readings'))
    }

    if conn and kanji_data.get('kanji_id'):
        kanji_data['example_words'] = get_example_words_for_kanji(kanji_data['kanji_id'], conn)
    else:
        kanji_data['example_words'] = []
        # Optional: print a warning if conn is None, though it should always be provided by calling functions
        # if not conn: print("Warning: No DB connection passed to _row_to_dict for fetching example words.")

    return kanji_data

@main_bp.route('/')
def index_page():
    return render_template('index.html')

@main_bp.route('/data/svgs/<path:filename>')
def serve_svg(filename):
    project_root = Path(current_app.root_path).parent
    svg_dir = project_root / 'data' / 'kanjivg_svgs'
    if not (svg_dir / filename).is_file():
        abort(404)
    return send_from_directory(str(svg_dir), filename, mimetype='image/svg+xml')

@api_bp.route('/kanji/<string:kanji_char>', methods=['GET'])
def get_kanji(kanji_char):
    kanji_dict = get_kanji_from_db(kanji_char) 
    if kanji_dict is None:
        return jsonify({'error': f'Kanji "{kanji_char}" not found'}), 404
    return jsonify(kanji_dict)

@api_bp.route('/search/kanji', methods=['GET'])
def search_kanji():
    query_term = request.args.get('query', '').strip()
    if not query_term:
        return jsonify({'error': 'Search query cannot be empty'}), 400
    
    results = search_kanjis_in_db(query_term) 
    return jsonify(results)

# ... (rest of the file, if any, including blueprint registration if done here)
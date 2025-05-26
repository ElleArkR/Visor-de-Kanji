from flask import Blueprint, jsonify, request, abort, render_template, current_app, send_from_directory
import os
from . import db # Assuming db.py is in the same directory (app/)

# Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Blueprint for main application routes (serving HTML)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index_page():
    return render_template('index.html')

@main_bp.route('/data/svgs/<path:filename>')
def serve_svg(filename):
    """Serves SVG files from the kanjivg_svgs data directory."""
    # Correctly construct the path to the 'data/kanjivg_svgs' directory
    # The 'app' directory is current_app.root_path
    # We need to go one level up to 'kanji_project' and then into 'data/kanjivg_svgs'
    svg_dir = os.path.abspath(os.path.join(current_app.root_path, '..', 'data', 'kanjivg_svgs'))
    return send_from_directory(svg_dir, filename)

def _comma_separated_to_list(comma_str):
    """Converts a comma-separated string to a list of strings. Returns None if input is None."""
    if comma_str is None:
        return None
    return [s.strip() for s in comma_str.split(',') if s.strip()]

def _row_to_dict(row):
    """Converts a sqlite3.Row object to a dictionary, processing list-like fields."""
    if not row:
        return None
    
    kanji_dict = dict(row) # Convert sqlite3.Row to a regular dict
    
    # Convert comma-separated strings back to lists
    for field in ['meanings', 'kun_readings', 'on_readings']:
        if kanji_dict.get(field):
            kanji_dict[field] = _comma_separated_to_list(kanji_dict[field])
        else:
            # Ensure the field exists in the output, even if it's None or empty
            kanji_dict[field] = [] if kanji_dict.get(field) is None else _comma_separated_to_list(kanji_dict[field])


    # Ensure all expected fields are present, even if None from DB
    expected_fields = ["id", "kanji_char", "unicode", "meanings", "kun_readings", 
                       "on_readings", "stroke_count", "grade", "jlpt_level", "svg_filename"]
    for ef in expected_fields:
        if ef not in kanji_dict:
            kanji_dict[ef] = None
            if ef in ['meanings', 'kun_readings', 'on_readings']: # Ensure list fields are empty lists if None
                 kanji_dict[ef] = []


    return kanji_dict

@api_bp.route('/kanji/<string:kanji_char>', methods=['GET'])
def get_kanji(kanji_char):
    """Endpoint to get a specific kanji by its character."""
    conn = db.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kanjis WHERE kanji_char = ?", (kanji_char,))
    row = cursor.fetchone()
    
    if row is None:
        return jsonify({"error": "Kanji not found"}), 404
        
    kanji_details = _row_to_dict(row)

    if kanji_details: # If kanji was found and processed
        kanji_id = kanji_details.get("id")
        if kanji_id is not None:
            cursor.execute("""
                SELECT w.word, w.reading, w.meaning_es, w.jlpt_level_word
                FROM example_words w
                JOIN kanji_example_word_assoc a ON w.id = a.word_id
                WHERE a.kanji_id = ?
                ORDER BY w.jlpt_level_word DESC, w.id
            """, (kanji_id,))
            example_word_rows = cursor.fetchall()
            
            example_words_list = []
            for word_row in example_word_rows:
                example_words_list.append(dict(word_row)) # Convert sqlite3.Row to dict
            
            kanji_details["example_words"] = example_words_list
        else:
            kanji_details["example_words"] = [] # Should not happen if kanji_details is valid
    
    return jsonify(kanji_details)

@api_bp.route('/search/kanji', methods=['GET'])
def search_kanji():
    """Endpoint to search for kanji by character or meaning."""
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    conn = db.get_db()
    cursor = conn.cursor()
    
    results = []
    
    # Search by exact kanji_char match
    cursor.execute("SELECT * FROM kanjis WHERE kanji_char = ?", (query,))
    rows = cursor.fetchall()
    for row in rows:
        results.append(_row_to_dict(row))
        
    # Search by meaning (case-insensitive substring match)
    # Ensure query is lowercased for the LIKE comparison if the SQL function LOWER is not universally available or performant
    # For SQLite, LOWER() function works well.
    # The comma-separated nature of 'meanings' makes direct SQL LIKE tricky for individual meanings.
    # Fetching all and filtering in Python is safer for the MVP if SQL LIKE on comma-list is complex.
    # However, a simple LIKE should catch most cases.
    
    # To avoid adding duplicates if a kanji matched by char AND meaning
    existing_ids = {res['id'] for res in results if res and 'id' in res}

    # Search by meaning (case-insensitive substring match)
    # Using INSTR for substring search which is common in SQLite, and LOWER for case-insensitivity.
    # This query searches if the lowercase query string is a substring of the lowercase meanings column.
    cursor.execute("SELECT * FROM kanjis WHERE INSTR(LOWER(meanings), LOWER(?)) > 0", (query,))
    rows_meaning = cursor.fetchall()

    for row_m in rows_meaning:
        if row_m['id'] not in existing_ids: # Avoid duplicates
            results.append(_row_to_dict(row_m))
            existing_ids.add(row_m['id']) # Add new id to set

    return jsonify(results)

# The main app __init__.py should have registered the main blueprint.
# Example: app.register_blueprint(routes.bp)
# And also db.init_app(app)
# The run.py should correctly import and run the app from create_app()
# The database file kanji.db should be in the kanji_project directory.
# The SVG files should be handled separately if they need to be served.
# This setup assumes init_db.py has been run to create and populate kanji.db.

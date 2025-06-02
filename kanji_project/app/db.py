import sqlite3
import pathlib
import os # os is needed if DATABASE_PATH construction relies on it, but pathlib is preferred.
from flask import current_app, g

# Define Paths using pathlib for robustness
# Assuming this db.py is in 'kanji_project/app/'
# So, BASE_PROJECT_DIR should be 'kanji_project'
APP_DIR = pathlib.Path(__file__).resolve().parent
BASE_PROJECT_DIR = APP_DIR.parent # This should point to kanji_project
DATABASE_PATH = BASE_PROJECT_DIR / "kanji.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(f"Database file not found at {DATABASE_PATH}")
    conn = sqlite3.connect(str(DATABASE_PATH)) # Ensure DATABASE_PATH is a string for connect
    conn.row_factory = sqlite3.Row # Optional: to access columns by name
    return conn

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        db_path = get_db_path()
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # Allows accessing columns by name
    return g.db

def close_db(e=None):
    """Closes the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Register database functions with the Flask app. This is called by the application factory."""
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command) # If you want a CLI command 'flask init-db'
    # For now, init_db.py script is used manually.

# Optional: If you want a CLI command to initialize the DB (requires init_db.py logic here)
# def init_db():
#     db = get_db()
#     # Here you would execute the schema creation logic, e.g., from init_db.py
#     # For simplicity, this is handled by the separate init_db.py script for now.

# @click.command('init-db')
# def init_db_command():
#     """Clear existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

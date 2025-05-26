import sqlite3
import os
from flask import current_app, g

DATABASE_NAME = "kanji.db" # Should be in the instance folder or project root
# Construct the path relative to the instance folder if using one, or project root.
# For now, assuming it's in the project root as per init_db.py.
DATABASE_PATH = os.path.join(current_app.root_path, '..', DATABASE_NAME) if current_app else os.path.join('kanji_project', DATABASE_NAME)
# A better approach for DATABASE_PATH if not using instance folder:
# DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), DATABASE_NAME)


def get_db_path():
    """Returns the absolute path to the database file."""
    # Assuming kanji_project is the root directory of the project
    # and this script (db.py) is in kanji_project/app/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(project_root, 'kanji_project', DATABASE_NAME)

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
#     print("Database initialized (or schema ensured).")

# @click.command('init-db')
# def init_db_command():
#     """Clear existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')

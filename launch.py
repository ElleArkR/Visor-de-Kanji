import os
import subprocess
import sys
from pathlib import Path
import sqlite3

# Define Paths
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR / 'kanji_project'
VENV_DIR = PROJECT_DIR / 'venv'
REQUIREMENTS_FILE = PROJECT_DIR / 'requirements.txt'
RUN_PY_FILE = PROJECT_DIR / 'run.py'
DATA_DIR = PROJECT_DIR / 'data'
KANJI_DATA_JSON = DATA_DIR / 'kanji_data.json' # Updated path
DB_FILE = PROJECT_DIR / 'kanji.db'
FETCH_SCRIPT = PROJECT_DIR / 'scripts' / 'fetch_kanji_data.py'
INIT_DB_SCRIPT = PROJECT_DIR / 'scripts' / 'init_db.py'
POPULATE_EXAMPLES_SCRIPT = PROJECT_DIR / 'scripts' / 'populate_examples.py'
DOWNLOAD_SVGS_SCRIPT = PROJECT_DIR / 'scripts' / 'download_svgs.py'
SVG_DIR = PROJECT_DIR / 'data' / 'kanjivg_svgs'


# Determine Virtual Environment Python and Pip Executables
if sys.platform == 'win32':
    python_exe_in_venv = VENV_DIR / 'Scripts' / 'python.exe'
    pip_exe_in_venv = VENV_DIR / 'Scripts' / 'pip.exe'
else:
    python_exe_in_venv = VENV_DIR / 'bin' / 'python'
    pip_exe_in_venv = VENV_DIR / 'bin' / 'pip'

# Function to Create Virtual Environment
def create_venv():
    """Creates a virtual environment if it doesn't exist."""
    if not VENV_DIR.exists() or not python_exe_in_venv.exists():
        print(f"Creating virtual environment in {VENV_DIR}...")
        try:
            process_result = subprocess.run([sys.executable, '-m', 'venv', str(VENV_DIR)], check=True, capture_output=True, text=True)
            if process_result.returncode != 0:
                print(f"Error creating virtual environment: {process_result.stderr}")
                sys.exit(1)
            print("Virtual environment created.")
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The Python executable '{sys.executable}' was not found.")
            sys.exit(1)
    else:
        print(f"Virtual environment found at {VENV_DIR}.")

# Function to Install Dependencies
def install_dependencies():
    """Installs dependencies from requirements.txt."""
    print(f"Installing/verifying dependencies from {REQUIREMENTS_FILE}...")
    if not REQUIREMENTS_FILE.exists():
        print(f"Error: {REQUIREMENTS_FILE} not found.")
        # Create an empty requirements.txt if it does not exist, as per project setup
        print(f"Creating an empty {REQUIREMENTS_FILE} as it was not found.")
        try:
            with open(REQUIREMENTS_FILE, 'w') as f:
                pass # Create an empty file
            print(f"{REQUIREMENTS_FILE} created.")
        except IOError as e:
            print(f"Error creating {REQUIREMENTS_FILE}: {e}")
            sys.exit(1)


    if not pip_exe_in_venv.exists():
        print(f"Error: pip executable not found at {pip_exe_in_venv}.")
        print("Please ensure the virtual environment was created correctly.")
        sys.exit(1)

    try:
        process_result = subprocess.run([str(pip_exe_in_venv), 'install', '-r', str(REQUIREMENTS_FILE)], check=True, capture_output=True, text=True)
        if process_result.returncode != 0:
            print(f"Error installing dependencies: {process_result.stderr}")
            sys.exit(1)
        print("Dependencies installed/verified.")
    except subprocess.CalledProcessError as e:
        # Allow for no requirements to be installed if requirements.txt is empty
        if "Requirement file contains no requirements" in e.stdout or "Requirement file contains no requirements" in e.stderr:
             print("No dependencies listed in requirements.txt.")
        elif e.returncode != 0 :
            print(f"Error installing dependencies: {e.stderr}")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The pip executable '{pip_exe_in_venv}' was not found.")
        sys.exit(1)


# Function to Run Application
def run_application():
    """Runs the Flask application."""
    print(f"Starting Flask application from {RUN_PY_FILE}...")
    if not RUN_PY_FILE.exists():
        print(f"Error: {RUN_PY_FILE} not found.")
        sys.exit(1)

    if not python_exe_in_venv.exists():
        print(f"Error: Python executable not found at {python_exe_in_venv}.")
        print("Please ensure the virtual environment was created correctly.")
        sys.exit(1)
    
    try:
        os.chdir(PROJECT_DIR)
        subprocess.run([str(python_exe_in_venv), str(RUN_PY_FILE.name)], cwd=PROJECT_DIR)
    except FileNotFoundError:
        print(f"Error: The Python executable '{python_exe_in_venv}' or run script '{RUN_PY_FILE.name}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while trying to run the application: {e}")
        sys.exit(1)
    finally:
        print("Flask application has stopped or could not be started.")

# Helper function to check if a table exists in the database
def check_db_table_exists(conn, table_name):
    """Checks if a specific table exists in the SQLite database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error when checking for table {table_name}: {e}")
        return False # Assume table doesn't exist or DB is inaccessible

# Function to Setup Database
def setup_database():
    """Ensures data directory exists, fetches Kanji data, and initializes the database if necessary."""
    print("Starting database setup...")

    # Step 1: Ensure DATA_DIR exists
    if not DATA_DIR.exists():
        print(f"Data directory {DATA_DIR} not found. Creating it...")
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True) # Using Path.mkdir
            print(f"Data directory {DATA_DIR} created.")
        except OSError as e:
            print(f"Error creating data directory {DATA_DIR}: {e}")
            sys.exit(1)
    else:
        print(f"Data directory {DATA_DIR} found.")

    # Step 2: Run fetch_kanji_data.py if necessary
    if not KANJI_DATA_JSON.exists():
        print(f"{KANJI_DATA_JSON} not found. Running {FETCH_SCRIPT.name}...")
        if not FETCH_SCRIPT.exists():
            print(f"Error: Fetch script {FETCH_SCRIPT} not found. Cannot proceed with data fetching.")
            sys.exit(1)
        
        try:
            # Prepare environment for the script
            script_env = os.environ.copy()
            script_env['PYTHONIOENCODING'] = 'utf-8'
            
            process_result = subprocess.run(
                [str(python_exe_in_venv), str(FETCH_SCRIPT)], 
                cwd=BASE_DIR, check=True, capture_output=True, text=True, env=script_env, encoding='utf-8'
            )
            print(f"{FETCH_SCRIPT.name} completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {FETCH_SCRIPT.name}: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The Python executable '{python_exe_in_venv}' or script '{FETCH_SCRIPT}' was not found.")
            sys.exit(1)
    else:
        print(f"{KANJI_DATA_JSON} found.")

    # Step 2.5: Run download_svgs.py if necessary
    # Check if SVG_DIR exists and is not empty
    svgs_missing = True
    if SVG_DIR.is_dir() and any(SVG_DIR.iterdir()):
        print(f"SVG directory {SVG_DIR} found and is not empty. Skipping SVG download.")
        svgs_missing = False
    elif not SVG_DIR.is_dir():
        print(f"SVG directory {SVG_DIR} not found.")
    else: # SVG_DIR exists but is empty
        print(f"SVG directory {SVG_DIR} found but is empty.")

    if svgs_missing:
        print(f"Running {DOWNLOAD_SVGS_SCRIPT.name} to download SVGs...")
        if not DOWNLOAD_SVGS_SCRIPT.exists():
            print(f"Error: SVG Download script {DOWNLOAD_SVGS_SCRIPT} not found. Cannot proceed.")
            sys.exit(1)
        
        try:
            script_env = os.environ.copy()
            script_env['PYTHONIOENCODING'] = 'utf-8'
            
            process_result = subprocess.run(
                [str(python_exe_in_venv), str(DOWNLOAD_SVGS_SCRIPT)],
                cwd=BASE_DIR, check=True, capture_output=True, text=True, env=script_env, encoding='utf-8'
            )
            # print(process_result.stdout) # Optional: print script output
            # if process_result.stderr: # Optional: print script error output
            #     print(f"Errors from {DOWNLOAD_SVGS_SCRIPT.name}:\n{process_result.stderr}", file=sys.stderr)
            print(f"{DOWNLOAD_SVGS_SCRIPT.name} completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {DOWNLOAD_SVGS_SCRIPT.name}: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The Python executable '{python_exe_in_venv}' or script '{DOWNLOAD_SVGS_SCRIPT}' was not found.")
            sys.exit(1)

    # Step 3: Run init_db.py and populate_examples.py if necessary
    db_needs_initialization = True
    if DB_FILE.exists():
        print(f"Database file {DB_FILE} found.")
        conn = None # Ensure conn is defined for finally block
        try:
            conn = sqlite3.connect(str(DB_FILE))
            if check_db_table_exists(conn, 'kanjis'):
                db_needs_initialization = False
                print("Database and 'kanjis' table found.")
            else:
                print("'kanjis' table not found in the database. Database will be initialized.")
        except sqlite3.Error as e:
            print(f"Error connecting to database {DB_FILE} or checking table: {e}. Will attempt to re-initialize.")
            db_needs_initialization = True # Force re-initialization on error
        finally:
            if conn:
                conn.close()
    else:
        print(f"Database file {DB_FILE} not found. Database will be initialized.")

    if db_needs_initialization:
        print("Database requires initialization. Running initialization scripts...")
        
        # Run init_db.py
        if not INIT_DB_SCRIPT.exists():
            print(f"Error: Init DB script {INIT_DB_SCRIPT} not found. Cannot proceed.")
            sys.exit(1)
        try:
            # Ensure script_env is defined for INIT_DB_SCRIPT, containing PYTHONIOENCODING='utf-8'
            script_env_init_db = os.environ.copy()
            script_env_init_db['PYTHONIOENCODING'] = 'utf-8'

            print(f"Running {INIT_DB_SCRIPT.name} with direct console output for debugging...")
            subprocess.run(
                [str(python_exe_in_venv), str(INIT_DB_SCRIPT)],
                cwd=BASE_DIR,
                env=script_env_init_db, 
                check=False # Allow script to run and print even if it has errors
            )
            # No process_result.stdout or .stderr to print here as output is direct to console
            # No explicit check for process_result.returncode as check=False
            print(f"{INIT_DB_SCRIPT.name} execution attempt finished.") # Indicate script has run
        except subprocess.CalledProcessError as e:
            print(f"Error running {INIT_DB_SCRIPT.name}: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The Python executable '{python_exe_in_venv}' or script '{INIT_DB_SCRIPT}' was not found.")
            sys.exit(1)

        # Run populate_examples.py
        if not POPULATE_EXAMPLES_SCRIPT.exists():
            print(f"Error: Populate examples script {POPULATE_EXAMPLES_SCRIPT} not found. Cannot proceed.")
            sys.exit(1)
        try:
            # For POPULATE_EXAMPLES_SCRIPT, keep current settings (capture output) unless specified otherwise
            # If it also needs PYTHONIOENCODING, its script_env should be set similarly
            script_env_populate_db = os.environ.copy()
            script_env_populate_db['PYTHONIOENCODING'] = 'utf-8'
            process_result = subprocess.run(
                [str(python_exe_in_venv), str(POPULATE_EXAMPLES_SCRIPT)],
                cwd=BASE_DIR, check=True, capture_output=True, text=True, env=script_env_populate_db, encoding='utf-8'
            )
            print(f"{POPULATE_EXAMPLES_SCRIPT.name} completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {POPULATE_EXAMPLES_SCRIPT.name}: {e.stderr}")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The Python executable '{python_exe_in_venv}' or script '{POPULATE_EXAMPLES_SCRIPT}' was not found.")
            sys.exit(1)
        print("Database setup complete.")
    else:
        print("Database already appears to be set up.")

# Main Execution Block
if __name__ == '__main__':
    # Ensure project directory exists, create if not. This is good practice.
    if not PROJECT_DIR.exists():
        print(f"Project directory {PROJECT_DIR} not found. Creating it...")
        try:
            PROJECT_DIR.mkdir(parents=True, exist_ok=True)
            print(f"Project directory {PROJECT_DIR} created.")
        except OSError as e:
            print(f"Error creating project directory {PROJECT_DIR}: {e}")
            sys.exit(1)
            
    create_venv()
    install_dependencies()
    setup_database() # Call the new database setup function
    run_application()

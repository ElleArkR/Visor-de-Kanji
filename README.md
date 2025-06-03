# Proyecto Kanji Flask

Este es un proyecto de aplicación web Flask diseñado como una herramienta de aprendizaje de Kanji. Permite a los usuarios ver caracteres Kanji, sus significados, lecturas, número de trazos, palabras de ejemplo y visualizaciones SVG de los Kanji.

## Tecnologías Utilizadas

*   **Framework Web:** Flask
*   **Base de Datos:** SQLite
*   **Lenguaje de Programación:** Python

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

*   **`kanji_project/`**: Directorio principal del proyecto.
    *   **`app/`**: Contiene la lógica principal de la aplicación Flask.
        *   `__init__.py`: Inicializa la aplicación Flask, la base de datos y registra las rutas.
        *   `routes.py`: Define los endpoints de la API (por ejemplo, para obtener datos de Kanji, buscar) y las rutas para las páginas web.
        *   `db.py`: Gestiona la conexión con la base de datos SQLite (`kanji.db`).
        *   `static/`: Almacena los archivos estáticos como CSS (`style.css`) y JavaScript (`script.js`).
        *   `templates/`: Contiene las plantillas HTML (`index.html`).
        *   `translation_data.py`: Contiene el diccionario `TRANSLATIONS_DICT` para las traducciones de términos de inglés a español.
        *   `models.py`: Actualmente vacío, destinado a los modelos de base de datos (por ejemplo, si se utiliza un ORM como SQLAlchemy).
    *   **`scripts/`**: Incluye scripts de Python para diversas tareas de backend:
        *   `init_db.py`: Inicializa el esquema de la base de datos.
        *   `fetch_kanji_data.py`: Obtiene datos de Kanji de fuentes externas para poblar la base de datos.
        *   `populate_examples.py`: Añade palabras de ejemplo a la base de datos.
        *   `download_svgs.py`: Descarga archivos SVG para los caracteres Kanji.
        *   `set_svg_animation_loop.py`: Modifica archivos SVG, posiblemente para animaciones.
    *   **`data/`** (Directorio conceptual, los datos como `kanji.db` y los SVGs residen dentro de `kanji_project` o subdirectorios como `kanji_project/data/kanjivg_svgs/` según la configuración de los scripts): Almacena los archivos de datos, como la base de datos SQLite y las imágenes SVG.
    *   `run.py`: El punto de entrada para iniciar el servidor de desarrollo de Flask.
    *   `config.py`: Almacena la configuración de la aplicación, como la URI de la base de datos.
    *   `requirements.txt`: Lista las dependencias de paquetes de Python.
    *   `flask_app.log`: Archivo de log generado por la aplicación.

## Configuración y Primera Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto por primera vez:

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO> 
    ```
    (Reemplaza `<URL_DEL_REPOSITORIO>` y `<NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO>` con los valores correctos. El directorio del proyecto probablemente sea `AIDE-Code-Helper-Testing-Playground` si estás clonando este repo específico, y luego deberías navegar a `kanji_project` o ejecutar los scripts desde el directorio raíz especificando la ruta completa, ej. `python kanji_project/scripts/init_db.py`)

2.  **Crear y Activar un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    ```
    En Windows:
    ```bash
    venv\Scripts\activate
    ```
    En macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    Asegúrate de que tu entorno virtual esté activado.
    ```bash
    pip install -r kanji_project/requirements.txt
    ```

4.  **Inicializar la Base de Datos:**
    Este script crea el archivo `kanji.db` y las tablas necesarias.
    ```bash
    python kanji_project/scripts/init_db.py
    ```

5.  **Poblar la Base de Datos:**
    Ejecuta los siguientes scripts para llenar la base de datos con datos de Kanji, palabras de ejemplo y descargar los SVGs. Se recomienda ejecutarlos en este orden:
    *   Descargar los datos principales de los Kanji:
        ```bash
        python kanji_project/scripts/fetch_kanji_data.py
        ```
    *   Poblar con palabras de ejemplo:
        ```bash
        python kanji_project/scripts/populate_examples.py
        ```
    *   Descargar los archivos SVG de los Kanji (esto puede tardar un tiempo y requiere conexión a internet):
        ```bash
        python kanji_project/scripts/download_svgs.py
        ```
        *Nota: El script `set_svg_animation_loop.py` existe para modificar los SVGs, puedes ejecutarlo si es necesario después de la descarga.*
        ```bash
        # python kanji_project/scripts/set_svg_animation_loop.py 
        ```

6.  **Ejecutar la Aplicación:**
    Una vez que la base de datos esté configurada y poblada:
    ```bash
    python kanji_project/run.py
    ```
    La aplicación debería estar disponible en `http://127.0.0.1:5000/` o en el puerto que Flask indique.

## Endpoints de la API

La aplicación proporciona los siguientes endpoints de API:

*   `GET /api/kanji/<kanji_char>`: Obtiene datos detallados para un carácter Kanji específico.
*   `GET /api/search/kanji?query=<termino>`: Busca Kanjis basados en un término de consulta (puede ser el carácter, significado, lectura, etc.).

## Scripts Utilitarios

El directorio `scripts/` contiene varias utilidades para la gestión de datos. Ya se ha cubocado su uso principal para la configuración inicial. Si necesitas reinicializar o actualizar datos, puedes volver a ejecutar estos scripts, teniendo en cuenta que algunos pueden eliminar datos existentes o tardar mucho tiempo en completarse.

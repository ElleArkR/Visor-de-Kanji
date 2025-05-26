@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Define el nombre de la carpeta del proyecto y del entorno virtual
SET PROJECT_DIR=kanji_project
SET VENV_DIR=%PROJECT_DIR%\venv

ECHO Verificando la instalacion de Python...

REM Intenta encontrar Python. Primero busca python.exe, luego py.exe
WHERE python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    WHERE py >nul 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        ECHO ERROR: Python no se encuentra en el PATH.
        ECHO Por favor, instala Python (desde python.org o la Microsoft Store) y asegurate de que este anadido al PATH.
        PAUSE
        EXIT /B 1
    ) ELSE (
        SET PYTHON_EXE=py
    )
) ELSE (
    SET PYTHON_EXE=python
)
ECHO Python encontrado: %PYTHON_EXE%

ECHO Iniciando Buscador de Kanjis en Espanol...

REM Verifica si existe el directorio del proyecto
IF NOT EXIST "%PROJECT_DIR%" (
    ECHO ERROR: El directorio del proyecto '%PROJECT_DIR%' no se encuentra.
    ECHO Asegurate de que el script .bat este en el directorio correcto.
    PAUSE
    EXIT /B 1
)

REM Verifica si el entorno virtual ya existe
IF NOT EXIST "%VENV_DIR%\Scripts\activate.bat" (
    ECHO Creando entorno virtual en '%VENV_DIR%'...
    %PYTHON_EXE% -m venv "%VENV_DIR%"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO ERROR: No se pudo crear el entorno virtual.
        PAUSE
        EXIT /B 1
    )
    ECHO Entorno virtual creado.
) ELSE (
    ECHO Entorno virtual encontrado en '%VENV_DIR%'.
)

REM Activa el entorno virtual
ECHO Activando entorno virtual...
CALL "%VENV_DIR%\Scripts\activate.bat"

REM Instala/actualiza las dependencias desde requirements.txt
ECHO Instalando/verificando dependencias desde '%PROJECT_DIR%\requirements.txt'...
IF NOT EXIST "%PROJECT_DIR%\requirements.txt" (
    ECHO ERROR: El archivo '%PROJECT_DIR%\requirements.txt' no se encuentra.
    PAUSE
    EXIT /B 1
)
%PYTHON_EXE% -m pip install -r "%PROJECT_DIR%\requirements.txt"
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: No se pudieron instalar las dependencias.
    PAUSE
    EXIT /B 1
)
ECHO Dependencias instaladas/verificadas.

REM Cambia al directorio del proyecto y ejecuta la aplicacion
ECHO Iniciando la aplicacion Flask...
CD /D "%PROJECT_DIR%"
%PYTHON_EXE% run.py

ECHO La aplicacion Flask se ha detenido o no pudo iniciarse.
PAUSE
ENDLOCAL

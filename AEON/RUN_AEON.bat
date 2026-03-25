
@echo off
REM Fixes python path and activates venv temporarily if possible, then runs AEON module

SET CURRENT_DIR=%~dp0
SET VENV_PATH=%CURRENT_DIR%venv
SET PYTHONPATH=%CURRENT_DIR%

REM Process .env (basic check)
if not exist .env (
    echo [WARNING] .env file not found. System may fail.
    copy .env.example .env
    echo Created .env from example. Please edit it!
    pause
)

REM Use python from venv if exists, else system python
if exist "%VENV_PATH%\Scripts\python.exe" (
    "%VENV_PATH%\Scripts\python.exe" -m aeon
) else (
    echo Venv not found, trying system python...
    python -m aeon
)

pause

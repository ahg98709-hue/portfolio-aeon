@echo off
setlocal
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m aeon.gui.main_window
pause

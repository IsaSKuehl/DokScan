@echo off
REM Aktiviere virtuelle Umgebung
call venv\Scripts\activate.bat

REM Installiere Pakete
python -m pip install -r requirements.txt

REM Starte Programm
python src/main.py

pause
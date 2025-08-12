@echo off
cd /d "C:\projects\Zwift"
poetry run python src\move_zwift_files.py
poetry run python src\fitfile_etl.py
echo Scripts finished. Press any key to close this window.
pause >nul

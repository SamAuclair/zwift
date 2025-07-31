@echo off
cd /d "C:\projects\Zwift"
poetry run python src\move_zwift_files.py
echo.
echo Script finished. Press any key to close this window.
pause >nul

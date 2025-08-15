@echo off
echo Starting Activity Report Generator...
python gui_app.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start the application
    echo Make sure you have run setup.bat first
    pause
)
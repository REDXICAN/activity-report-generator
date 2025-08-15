@echo off
echo Activity Report Generator Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Installing required packages...
echo.

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install some packages
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To run the application:
echo   - GUI Mode: python gui_app.py
echo   - CLI Mode: python main.py
echo.
pause
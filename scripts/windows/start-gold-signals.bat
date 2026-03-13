@echo off
echo 🥇 GenX FX Gold Signal Generator
echo ================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Install required packages
echo 📦 Installing dependencies...
pip install requests fastapi uvicorn google-generativeai
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Set environment variables (replace with your actual keys)
set GEMINI_API_KEY=your_gemini_api_key_here
set EXNESS_LOGIN=your_exness_login
set EXNESS_PASSWORD=your_exness_password
set EXNESS_SERVER=Exness-MT5Real24

REM Create logs directory
if not exist "logs" mkdir logs

REM Start the gold signal generator
echo 🚀 Starting Gold Signal Generator...
echo.
echo 📊 Features:
echo   • Gold pairs: XAUUSD, XAUEUR, XAUGBP, XAUAUD
echo   • AI-powered analysis with Gemini
echo   • VPS integration: http://34.71.143.222:8080
echo   • Local API: http://localhost:8080
echo   • Signal interval: 30 seconds
echo   • Min confidence: 75%%
echo.
echo 📡 Output:
echo   • MT4_Signals.csv (for EA consumption)
echo   • VPS API endpoint
echo   • Local API endpoint
echo.
echo Press Ctrl+C to stop
echo ================================
echo.

python gold-signal-generator.py

echo.
echo 🛑 Gold Signal Generator stopped
pause

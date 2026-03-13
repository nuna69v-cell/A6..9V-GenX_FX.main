@echo off
echo 🚀 GenX FX 24/7 Backend Service Launcher
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn, requests, google.generativeai" >nul 2>&1
if errorlevel 1 (
    echo ❌ Missing required packages
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Set environment variables
set GEMINI_API_KEY=your_gemini_api_key_here
set EXNESS_LOGIN=your_exness_login
set EXNESS_PASSWORD=your_exness_password
set EXNESS_SERVER=Exness-MT5Real24
set SECRET_KEY=your_secret_key_here

REM Create logs directory
if not exist "logs" mkdir logs

REM Start the 24/7 backend service
echo 🚀 Starting GenX FX 24/7 Backend Service...
echo.
echo 📊 Features:
echo   • Gold trading signal generation
echo   • VPS communication (34.71.143.222:8080)
echo   • EA communication (port 9090)
echo   • FastAPI server (port 8080)
echo   • AI-powered analysis with Gemini
echo.
echo 🌐 Access URLs:
echo   • API: http://localhost:8080
echo   • Docs: http://localhost:8080/docs
echo   • Health: http://localhost:8080/health
echo   • Signals: http://localhost:8080/api/v1/predictions
echo.
echo 📡 VPS Integration:
echo   • Sending signals to: http://34.71.143.222:8080
echo   • EA Communication: localhost:9090
echo.
echo Press Ctrl+C to stop the service
echo ========================================
echo.

python genx_24_7_backend.py

echo.
echo 🛑 GenX FX 24/7 Backend Service stopped
pause

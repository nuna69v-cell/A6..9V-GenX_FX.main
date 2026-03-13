@echo off
echo ========================================
echo Starting Uptime Kuma Monitoring
echo ========================================
echo.

REM Navigate to project root
cd /d "%~dp0"

echo Launching Uptime Kuma...
docker-compose -f docker-compose.uptime.yml up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start Uptime Kuma
    echo Make sure Docker Desktop is running
    pause
    goto :EOF
)

echo.
echo ========================================
echo Uptime Kuma is running!
echo ========================================
echo.
echo Access the dashboard at: http://localhost:3001
echo Create your admin account on first login.
echo.
pause

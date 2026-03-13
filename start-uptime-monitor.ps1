# Start Uptime Kuma Monitoring
# Sets up local monitoring of Docker containers, ping, and hardware status

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Uptime Kuma Monitoring" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if Docker Desktop is running
Write-Host "Checking Docker Desktop..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Desktop is NOT running" -ForegroundColor Red
    Write-Host "  Please start Docker Desktop first!" -ForegroundColor Yellow
    Exit
}

Write-Host ""
Write-Host "Launching Uptime Kuma..." -ForegroundColor Yellow
docker-compose -f docker-compose.uptime.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Uptime Kuma is running!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Access the dashboard at: " -NoNewline
    Write-Host "http://localhost:3001" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Initial Setup Guide:" -ForegroundColor Yellow
    Write-Host "1. Create your admin account on first login" -ForegroundColor White
    Write-Host "2. Add a 'Docker Container' monitor" -ForegroundColor White
    Write-Host "   - Docker Host: Local Docker socket" -ForegroundColor Gray
    Write-Host "   - Container Name: (e.g., genx-api, genx-discord-bot)" -ForegroundColor Gray
    Write-Host "3. Add a 'Ping' monitor for external IP/domains" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✗ Failed to start Uptime Kuma" -ForegroundColor Red
}

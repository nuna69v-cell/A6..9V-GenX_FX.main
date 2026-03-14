<#
.SYNOPSIS
    Automates setting up OpenSSH Server on Windows 11 for mobile SSH access via Termius.
.DESCRIPTION
    This script installs the OpenSSH Server capability, configures the SSH daemon for
    key-based authentication, ensures the authorized_keys file exists, sets up the
    Windows Firewall, and starts the SSH service.

    Optimized for the user NUNA to connect from Termius (Port 22, SSH).
#>

# Ensure script is run as Administrator
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "Please run this script as an Administrator."
    Exit
}

Write-Host "⚡ Bolt's High-Speed Command Line (SSH) Setup" -ForegroundColor Cyan

# 1. Install OpenSSH Server if it's not installed
$sshServer = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($sshServer.State -ne 'Installed') {
    Write-Host "[1/5] Installing OpenSSH Server capability..." -ForegroundColor Yellow
    Add-WindowsCapability -Online -Name $sshServer.Name
    Write-Host "OpenSSH Server installed successfully." -ForegroundColor Green
} else {
    Write-Host "[1/5] OpenSSH Server is already installed." -ForegroundColor Green
}

# 2. Start the sshd service and configure it to start automatically
Write-Host "[2/5] Configuring SSH service..." -ForegroundColor Yellow
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
Write-Host "SSH service is running and set to Automatic." -ForegroundColor Green

# 3. Ensure the Firewall rule is enabled for Port 22
Write-Host "[3/5] Verifying Firewall Rules for Port 22..." -ForegroundColor Yellow
if (!(Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue | Select-Object Name, Enabled)) {
    Write-Host "Firewall Rule 'OpenSSH-Server-In-TCP' does not exist, creating it..." -ForegroundColor Yellow
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
} else {
    Write-Host "Firewall rule already exists." -ForegroundColor Green
}

# 4. Configure sshd_config for Key-Based Authentication
$sshdConfigPath = "$env:ProgramData\ssh\sshd_config"
Write-Host "[4/5] Configuring sshd_config for Key-Based Authentication..." -ForegroundColor Yellow

if (Test-Path $sshdConfigPath) {
    $configContent = Get-Content $sshdConfigPath

    # Ensure PubkeyAuthentication is yes
    $configContent = $configContent -replace '^#?PubkeyAuthentication\s+.*', 'PubkeyAuthentication yes'

    # We leave PasswordAuthentication intact or explicitly allow it as fallback,
    # but ensure key-based works.
    $configContent = $configContent -replace '^#?PasswordAuthentication\s+.*', 'PasswordAuthentication yes'

    # Comment out the Administrators authorized_keys file so it uses the one in the user's profile
    $configContent = $configContent -replace '^(Match Group administrators)', '#$1'
    $configContent = $configContent -replace '^(       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys)', '#$1'

    $configContent | Set-Content $sshdConfigPath

    # Restart the service to apply changes
    Restart-Service sshd
    Write-Host "sshd_config updated and service restarted." -ForegroundColor Green
} else {
    Write-Warning "Could not find sshd_config at $sshdConfigPath"
}

# 5. Setup the .ssh directory and authorized_keys for NUNA
Write-Host "[5/5] Preparing ~/.ssh/authorized_keys..." -ForegroundColor Yellow
$userProfile = $env:USERPROFILE
$sshDir = Join-Path -Path $userProfile -ChildPath ".ssh"
$authKeysPath = Join-Path -Path $sshDir -ChildPath "authorized_keys"

if (-not (Test-Path $sshDir)) {
    New-Item -Path $sshDir -ItemType Directory -Force | Out-Null
    Write-Host "Created .ssh directory at $sshDir" -ForegroundColor Green
}

if (-not (Test-Path $authKeysPath)) {
    New-Item -Path $authKeysPath -ItemType File -Force | Out-Null
    Write-Host "Created authorized_keys file at $authKeysPath" -ForegroundColor Green
} else {
    Write-Host "authorized_keys file already exists at $authKeysPath" -ForegroundColor Green
}

# Fix permissions on authorized_keys to be secure (Administrators, SYSTEM, and Owner only)
icacls.exe $sshDir /inheritance:r /grant "SYSTEM:(F)" /grant "Administrators:(F)" /grant "$env:USERNAME:(F)" | Out-Null
icacls.exe $authKeysPath /inheritance:r /grant "SYSTEM:(F)" /grant "Administrators:(F)" /grant "$env:USERNAME:(F)" | Out-Null

Write-Host ""
Write-Host "✅ SSH Configuration Complete!" -ForegroundColor Green
Write-Host "Your laptop (192.168.1.10) is now ready to accept SSH connections on Port 22." -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Step:"
Write-Host "1. Open Termius on your phone."
Write-Host "2. Generate an SSH Key in Termius (Keychain -> + -> Generate Key)."
Write-Host "3. Copy the Public Key."
Write-Host "4. Paste the Public Key into this file on your laptop: $authKeysPath"
Write-Host "5. In Termius, edit the connection to 192.168.1.10, set Port to 22, Protocol to SSH, and attach the Key."
Write-Host "6. Connect instantly without a password!"

@echo off
echo ========================================
echo Setting up my drive projects on Windows 11...
echo ========================================

echo 1. Creating Environment Template
if not exist ".env" (
    copy .env.my_drive_projects.template .env
    echo Please fill in the required API keys in the generated .env file.
) else (
    echo .env file already exists.
)

echo 2. Downloading F-Droid APK
if not exist "downloads" mkdir downloads
powershell -Command "Invoke-WebRequest -Uri 'https://f-droid.org/F-Droid.apk' -OutFile 'downloads\F-Droid.apk'"
if exist "downloads\F-Droid.apk" (
    echo Successfully downloaded F-Droid.apk
) else (
    echo Failed to download F-Droid.apk
)

echo 3. Cloning Forgejo Runner
if not exist "forgejo-runner" (
    git clone https://code.forgejo.org/forgejo/runner.git forgejo-runner
    echo Successfully cloned Forgejo Runner.
) else (
    echo Forgejo Runner already exists.
)

echo 4. Wrapping up repositories
REM Add logic here for specific user repositories if needed.
REM git clone https://github.com/Mouy-leng172.git (Ensure valid repo URL)

echo ========================================
echo Environment setup complete for Windows 11!
echo ========================================

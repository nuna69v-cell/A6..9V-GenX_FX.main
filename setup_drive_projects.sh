#!/bin/bash
set -e

# Setup directories
PROJECTS_DIR="my_drive_projects"
mkdir -p "$PROJECTS_DIR"
cd "$PROJECTS_DIR"

echo "Setting up Google Drive projects..."

# Load .env if it exists in the parent directory
if [ -f "../.env" ]; then
    echo "Loading environment variables from ../.env..."
    export $(grep -v '^#' ../.env | xargs)
fi

GITHUB_USER="Mouy-leng172"

echo "Cloning A6..9V-GenX_FX.main.git..."
if [ ! -d "A6..9V-GenX_FX.main" ]; then
    git clone "https://forge.mql5.io/LengKundee/A6..9V-GenX_FX.main.git" || true
else
    echo "A6..9V-GenX_FX.main already exists. Skipping clone."
fi

# Clone specific repositories requested
echo "Cloning Autonomous-trading-Exness..."
if [ ! -d "Autonomous-trading-Exness" ]; then
    if [ -n "$GITHUB_TOKEN_2" ]; then
        git clone "https://${GITHUB_TOKEN_2}@github.com/${GITHUB_USER}/Autonomous-trading-Exness.git" || true
    else
        git clone "https://github.com/${GITHUB_USER}/Autonomous-trading-Exness.git" || true
    fi
else
    echo "Autonomous-trading-Exness already exists. Skipping clone."
fi

# FXPRO-broker is not found, but we attempt it just in case it becomes available
echo "Cloning FXPRO-broker..."
if [ ! -d "FXPRO-broker" ]; then
    if [ -n "$GITHUB_TOKEN_2" ]; then
        git clone "https://${GITHUB_TOKEN_2}@github.com/${GITHUB_USER}/FXPRO-broker.git" || true
    else
        git clone "https://github.com/${GITHUB_USER}/FXPRO-broker.git" || true
    fi
else
    echo "FXPRO-broker already exists. Skipping clone."
fi

echo "Cloning forgejo runner..."
if [ ! -d "runner" ]; then
    git clone "https://code.forgejo.org/forgejo/runner.git" || true
else
    echo "runner already exists. Skipping clone."
fi

echo "Downloading F-Droid.apk..."
if [ ! -f "F-Droid.apk" ]; then
    curl -s -O "https://f-droid.org/F-Droid.apk" || true
else
    echo "F-Droid.apk already exists."
fi

# Copy the .env setup to the repos
echo "Setting up environment..."
if [ -f "../.env.example" ]; then
    if [ -d "Autonomous-trading-Exness" ]; then
        cp ../.env.example "Autonomous-trading-Exness/.env.example" || true
    fi
    if [ -d "A6..9V-GenX_FX.main" ]; then
        cp ../.env.example "A6..9V-GenX_FX.main/.env.example" || true
    fi
else
    echo "No parent .env.example found, skipping."
fi

echo "Setup completed successfully."

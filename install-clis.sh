#!/bin/bash

# Configuration
ENV_FILE=".env"
REQUIRED_VARS=(
    "FORGEJO_TOKEN"
    "AWS_ACCESS_KEY"
    "JULES_API"
    "JULES_API_TOKEN"
)

echo "Running Credential Check..."

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE file not found!"
    echo "Please create it from .env.example"
    exit 1
fi

MISSING_VARS=0
for VAR in "${REQUIRED_VARS[@]}"; do
    VALUE=$(grep "^${VAR}=" "$ENV_FILE" | cut -d "=" -f2-)

    if [ -z "$VALUE" ]; then
        echo "Missing required credential: $VAR"
        MISSING_VARS=1
    else
        echo "Found: $VAR"
    fi
done

if [ $MISSING_VARS -eq 1 ]; then
    echo "Credential check failed. Please populate all missing variables in $ENV_FILE before starting the runner."
    exit 1
else
    echo "All required credentials verified."
    echo "Proceeding with CLI installation..."

    npm install -g @aws/q
    npm install -g @google/jules

    echo "Installation complete."
fi

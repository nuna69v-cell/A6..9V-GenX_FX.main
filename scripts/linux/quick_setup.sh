#!/bin/bash

# Quick Setup Script for GenX-FX Trading Platform
# This script runs the container setup with your provided credentials

set -e

echo "🚀 Starting GenX-FX Trading Platform Container Setup..."
echo "Using your provided credentials:"
echo "- GitHub: genxdbxfx1"
echo "- Docker Hub: genxdbx/genxdbxfx1"
echo "- MT5 Login: 279023502"
echo "- MT5 Server: Exness-MT5Real24"

# Run the container setup script
./container_setup.sh

echo "✅ Setup complete! Your trading platform is now running."
echo "📊 Access your application at: http://localhost:3000"
echo "📈 Monitoring dashboard at: http://localhost:3001"
echo "📚 API documentation at: http://localhost:8080/docs"
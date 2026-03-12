#!/bin/bash
# Extended setup for AWS Free Trial, Amazon Q CLI, Forge (Game Console/Linux), and Real-time Uptime

echo "🚀 Starting Extended Setup..."

# 1. Install AWS CLI v2
echo "📦 Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -q awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
aws --version

# 2. Install Amazon Q CLI (q)
echo "📦 Installing Amazon Q CLI..."
curl -Lo q "https://q.us-east-1.amazonaws.com/latest/amazon-q-cli"
chmod +x q
sudo mv q /usr/local/bin/q
q --version || echo "q installed but may require interactive setup."

# 3. Setup Repositories for Forge and MQL5
echo "📂 Cloning Target Repositories..."
cd /home/ec2-user || cd ~
git clone https://github.com/nuna69v-cell/all-in-one-desktop-mode-.git
git clone https://github.com/nuna69v-cell/MQL5-Google-Onedrive.git

# 4. Setup Real-time Update & Uptime (Uptime Kuma)
echo "📈 Setting up Synonym Uptime Monitoring (Uptime Kuma)..."
# Assuming Docker is installed (which the AWS Free Tier template handles)
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1

# 5. Game Console Hosting (Forge setup via generic Linux/Termux compatibility)
echo "🎮 Starting Forge setup for 'game console' compatibility..."
# Note: For actual game consoles, this usually means a jailed Linux (like PS4 Linux) or Android Termux.
# We ensure the Forge runner is isolated in a lightweight Alpine/Node Docker container.
docker run -d --name forge-runner --restart=unless-stopped \
    -v $(pwd)/all-in-one-desktop-mode-:/app \
    node:alpine \
    sh -c "cd /app && npm install --omit=dev && npm start"

echo "✅ Extended Setup Complete! AWS CLI, Amazon Q, Repositories, Uptime Kuma, and Forge are running."

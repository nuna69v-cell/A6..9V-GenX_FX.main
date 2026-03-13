#!/bin/bash
set -e

echo "🚀 Installing GitHub CLI (gh)..."
if ! command -v gh &> /dev/null; then
    type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
    sudo apt update
    sudo apt install gh -y
else
    echo "✅ GitHub CLI is already installed."
fi

echo "🚀 Installing GitLab CLI (glab)..."
# Just use standard download link to fetch the latest archive reliably
# Extract into /tmp to avoid overwriting repository files like README.md and LICENSE
cd /tmp
curl -sL https://gitlab.com/gitlab-org/cli/-/releases/v1.36.0/downloads/glab_1.36.0_Linux_x86_64.tar.gz -o glab.tar.gz
tar -xzf glab.tar.gz
sudo mv bin/glab /usr/local/bin/glab
rm -rf bin share glab.tar.gz README.md LICENSE
cd -
echo "✅ GitLab CLI is installed."

echo "🚀 Installing Jules CLI..."
# We have a jules.sh wrapper in the repository root. Make it executable and add to PATH.
if [ -f "./jules.sh" ]; then
    chmod +x ./jules.sh
    sudo cp ./jules.sh /usr/local/bin/jules
    echo "✅ Jules CLI installed (aliased to 'jules')."
else
    echo "⚠️ jules.sh not found in the current directory. Could not install."
fi

echo "🎉 All CLIs installed successfully!"

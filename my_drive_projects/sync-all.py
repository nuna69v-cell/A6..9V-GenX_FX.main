import requests
import json
import os
import subprocess
from dotenv import load_dotenv

# Load tokens from .env file
load_dotenv()

# Dictionary of accounts and their respective tokens
TOKENS = {
    "mouyleng172": os.getenv("GH_USER_TOKEN"),
    "LengKundee": os.getenv("GH_TOKEN")
}

# Base directory for storing cloned accounts
ACCOUNTS_DIR = os.path.join(os.getcwd(), "Accounts")

def get_repo_map_and_clone():
    master_map = {}

    # Ensure the base Accounts directory exists
    if not os.path.exists(ACCOUNTS_DIR):
        os.makedirs(ACCOUNTS_DIR)

    for user, token in TOKENS.items():
        if not token:
            print(f"⚠️ Skipping {user}: No token found in .env")
            continue

        print(f"\n🔍 Mapping and synchronizing repositories for: {user}...")

        url = "https://api.github.com/user/repos?per_page=100&affiliation=owner"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            repos = response.json()
            master_map[user] = []

            # Create specific user directory (e.g., Accounts/mouyleng172/)
            user_dir = os.path.join(ACCOUNTS_DIR, user)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            for r in repos:
                repo_name = r["name"]
                clone_url = r["clone_url"]

                # Add to Master Map
                master_map[user].append({
                    "name": repo_name,
                    "url": clone_url,
                    "branch": r["default_branch"],
                    "description": r["description"],
                    "private": r["private"]
                })

                # --- BULK CLONE LOGIC ---
                target_repo_dir = os.path.join(user_dir, repo_name)

                if os.path.exists(target_repo_dir):
                    print(f"  ✅ {repo_name} already exists. Skipping clone.")
                else:
                    print(f"  📥 Cloning {repo_name}...")

                    # Embed token into the clone URL for seamless authentication
                    auth_clone_url = clone_url.replace("https://", f"https://{token}@")

                    try:
                        # Run the git clone command quietly
                        subprocess.run(
                            ["git", "clone", auth_clone_url, target_repo_dir],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        print(f"     🎉 Successfully cloned {repo_name}.")
                    except subprocess.CalledProcessError as e:
                        print(f"     ❌ Failed to clone {repo_name}.")
                        # print(f"        Error: {e.stderr.decode('utf-8').strip()}")
        else:
            print(f"❌ Failed to fetch {user}: HTTP {response.status_code} - {response.text}")

    # Write the Master Map to JSON
    with open(".master-map.json", "w", encoding="utf-8") as f:
        json.dump(master_map, f, indent=4)

    print("\n🗺️ Master Map created and all repositories are synced to your local drive!")

if __name__ == "__main__":
    print("🚀 Starting GenX-FX Master Synchronizer...")
    get_repo_map_and_clone()

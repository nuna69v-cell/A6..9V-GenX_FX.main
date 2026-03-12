import requests
import json
import os
import subprocess
from dotenv import load_dotenv

# Load tokens from .env
load_dotenv()

# Tokens from your .env
TOKENS = {
    "mouyleng172": os.getenv("GH_USER_TOKEN"),
    "LengKundee": os.getenv("GH_TOKEN")
}

def get_repo_map():
    master_map = {}

    for user, token in TOKENS.items():
        print(f"Mapping repositories for: {user}...")
        url = f"https://api.github.com/users/{user}/repos"
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        # We need to handle pagination to get all repos
        repos = []
        page = 1
        while True:
            response = requests.get(f"{url}?per_page=100&page={page}", headers=headers)
            if response.status_code == 200:
                page_repos = response.json()
                if not page_repos:
                    break
                repos.extend(page_repos)
                page += 1
            else:
                print(f"Failed to fetch {user} (Page {page}): {response.status_code}")
                if response.status_code == 403:
                    print(response.text)
                break

        master_map[user] = [
            {
                "name": r["name"],
                "url": r["clone_url"],
                "branch": r.get("default_branch", "main"),
                "description": r.get("description", "")
            } for r in repos
        ]

    with open(".master-map.json", "w") as f:
        json.dump(master_map, f, indent=4)
    print("Master Map created successfully!")
    return master_map

def sync_repos(master_map):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    accounts_dir = os.path.join(base_dir, "Accounts")

    for user, repos in master_map.items():
        user_dir = os.path.join(accounts_dir, user)
        os.makedirs(user_dir, exist_ok=True)

        for repo in repos:
            repo_dir = os.path.join(user_dir, repo["name"])
            repo_url = repo["url"]

            # If token is available, we might want to use authenticated clone URL
            token = TOKENS.get(user)
            if token:
                # Insert token into clone url
                # https://github.com/user/repo.git -> https://token@github.com/user/repo.git
                if repo_url.startswith("https://"):
                    repo_url = repo_url.replace("https://", f"https://{token}@")

            print(f"Syncing {user}/{repo['name']}...")
            if os.path.exists(os.path.join(repo_dir, ".git")):
                # Pull if exists
                print(f"  Repo exists, pulling latest changes...")
                try:
                    subprocess.run(["git", "pull"], cwd=repo_dir, check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"  Error pulling {repo['name']}: {e.stderr}")
            else:
                # Clone if missing
                print(f"  Cloning repo...")
                try:
                    subprocess.run(["git", "clone", repo_url, repo_dir], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"  Error cloning {repo['name']}: {e.stderr}")

if __name__ == "__main__":
    # Change to the script's directory so .env and .master-map.json are found there
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    map_data = get_repo_map()
    sync_repos(map_data)

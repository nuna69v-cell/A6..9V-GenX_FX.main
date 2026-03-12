import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("sync.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("HotMeltingIron")

# Load environment variables
load_dotenv()

# Configuration
MASTER_MAP_FILE = ".master-map.json"
BASE_DIR = Path.cwd()
ACCOUNTS_DIR = BASE_DIR / "Accounts"
SYSTEMS_DIR = BASE_DIR / "Systems"

# Verify required tokens
TOKENS = {
    "mouyleng172": os.getenv("GH_USER_TOKEN"),
    "LengKundee": os.getenv("GH_TOKEN"),
}


def verify_environment():
    """Verify that required environment variables and directories exist."""
    missing_tokens = [user for user, token in TOKENS.items() if not token]
    if missing_tokens:
        logger.warning(f"Missing tokens for users: {', '.join(missing_tokens)}")
        logger.warning("Please configure GH_USER_TOKEN and GH_TOKEN in .env")

    # Ensure directories exist
    ACCOUNTS_DIR.mkdir(exist_ok=True)
    SYSTEMS_DIR.mkdir(exist_ok=True)

    for user in TOKENS.keys():
        (ACCOUNTS_DIR / user).mkdir(exist_ok=True)

    logger.info("Environment verification complete.")


def run_command(cmd, cwd=None, env=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env or os.environ,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(cmd)}")
        logger.error(f"Error output: {e.stderr}")
        return False, e.stderr


def get_repo_map():
    """Fetch repositories for configured users and save to master map."""
    master_map = {}

    for user, token in TOKENS.items():
        if not token:
            logger.warning(f"Skipping {user} due to missing token")
            continue

        logger.info(f"Mapping repositories for: {user}...")
        url = f"https://api.github.com/users/{user}/repos"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        # Handle pagination
        repos = []
        page = 1
        while True:
            paginated_url = f"{url}?page={page}&per_page=100"
            try:
                response = requests.get(paginated_url, headers=headers)
                response.raise_for_status()

                page_repos = response.json()
                if not page_repos:
                    break

                repos.extend(page_repos)
                page += 1
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch repositories for {user}: {e}")
                break

        if repos:
            master_map[user] = [
                {
                    "name": r["name"],
                    "url": r["clone_url"],
                    "ssh_url": r["ssh_url"],
                    "branch": r["default_branch"],
                    "description": r.get("description", ""),
                    "updated_at": r["updated_at"],
                }
                for r in repos
            ]
            logger.info(
                f"Successfully mapped {len(master_map[user])} repositories for {user}"
            )

    with open(MASTER_MAP_FILE, "w") as f:
        json.dump(master_map, f, indent=4)
    logger.info("Master Map updated successfully.")
    return master_map


def sync_repositories(master_map):
    """Clone or pull repositories based on the master map."""
    for user, repos in master_map.items():
        user_dir = ACCOUNTS_DIR / user
        token = TOKENS.get(user)

        if not token:
            continue

        logger.info(f"Syncing repositories for {user}...")

        for repo in repos:
            repo_name = repo["name"]
            repo_dir = user_dir / repo_name

            # Construct authenticated URL
            # Format: https://<token>@github.com/<user>/<repo>.git
            auth_url = repo["url"].replace("https://", f"https://{token}@")

            if repo_dir.exists():
                logger.info(f"[{user}/{repo_name}] Pulling latest changes...")
                success, output = run_command(["git", "pull"], cwd=repo_dir)
                if not success:
                    logger.error(
                        f"[{user}/{repo_name}] Failed to pull. Uncommitted changes?"
                    )
            else:
                logger.info(f"[{user}/{repo_name}] Cloning repository...")
                success, output = run_command(
                    ["git", "clone", auth_url, str(repo_dir)], cwd=user_dir
                )
                if success:
                    logger.info(f"[{user}/{repo_name}] Successfully cloned.")
                else:
                    logger.error(f"[{user}/{repo_name}] Failed to clone.")


def generate_gitconfig():
    """Generate gitconfig templates for conditional includes."""
    gitconfig_dir = BASE_DIR / ".gitconfig_templates"
    gitconfig_dir.mkdir(exist_ok=True)

    for user in TOKENS.keys():
        template_path = gitconfig_dir / f".gitconfig-{user}"
        with open(template_path, "w") as f:
            f.write(f"""[user]
    name = {user}
[credential]
    helper = store
""")
        logger.info(f"Generated gitconfig template for {user} at {template_path}")

    master_config = gitconfig_dir / ".gitconfig-master"
    with open(master_config, "w") as f:
        for user in TOKENS.keys():
            user_path = str(ACCOUNTS_DIR / user).replace("\\", "/")
            f.write(f"""[includeIf "gitdir:{user_path}/"]
    path = {str(gitconfig_dir / f".gitconfig-{user}").replace('\\', '/')}
""")
    logger.info(f"Generated master gitconfig template at {master_config}")
    logger.info(
        "To use these, append the contents of .gitconfig-master to your global ~/.gitconfig"
    )


def main():
    logger.info("Starting Hot Melting Iron Sync")
    verify_environment()

    logger.info("Step 1: Updating Master Map...")
    master_map = get_repo_map()

    if master_map:
        logger.info("Step 2: Syncing Repositories...")
        sync_repositories(master_map)

        logger.info("Step 3: Generating Git Configurations...")
        generate_gitconfig()

    logger.info("Hot Melting Iron Sync complete.")


if __name__ == "__main__":
    main()

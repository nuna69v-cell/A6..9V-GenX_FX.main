import json
import os
import subprocess
from pathlib import Path

# Paths
ACCOUNTS_DIR = os.path.join(os.getcwd(), "Accounts")
MAP_FILE = os.path.join(os.getcwd(), ".master-map.json")
MOUYLENG_DIR = os.path.join(ACCOUNTS_DIR, "mouyleng172")
LENGKUNDEE_DIR = os.path.join(ACCOUNTS_DIR, "LengKundee")

def run_command(command, cwd=None, hide_output=False):
    """Run a shell command."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            shell=True,
            stdout=subprocess.PIPE if hide_output else None,
            stderr=subprocess.PIPE if hide_output else None,
            text=True
        )
        return result.stdout if hide_output else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        if hide_output:
            print(f"   Error: {e.stderr.strip()}")
        return None

def check_uncommitted_changes(repo_path):
    """Check if there are uncommitted changes in the repository."""
    status = run_command("git status --porcelain", cwd=repo_path, hide_output=True)
    return status is not None and len(status.strip()) > 0

def cross_sync(dry_run=False):
    """
    Implements 'Hot Melting Iron' logic:
    Pulls updates from mouyleng172 repos and pushes them to corresponding LengKundee repos if they exist.
    (This is a basic structural demonstration, assuming the repos are cloned and have remotes set up).
    """
    if not os.path.exists(MAP_FILE):
        print(f"❌ Map file not found: {MAP_FILE}")
        return

    with open(MAP_FILE, "r") as f:
        master_map = json.load(f)

    # For each repo in mouyleng172, check if it exists in LengKundee
    mouy_repos = {repo["name"]: repo for repo in master_map.get("mouyleng172", [])}
    leng_repos = {repo["name"]: repo for repo in master_map.get("LengKundee", [])}

    print("🔥 Starting Hot Melting Iron Sync...")

    for repo_name in mouy_repos:
        if repo_name in leng_repos:
            print(f"\n🔄 Syncing matching repository: {repo_name}")
            mouy_repo_path = os.path.join(MOUYLENG_DIR, repo_name)
            leng_repo_path = os.path.join(LENGKUNDEE_DIR, repo_name)

            if not os.path.exists(mouy_repo_path) or not os.path.exists(leng_repo_path):
                 print(f"  ⚠️ Skipping {repo_name} - Not cloned locally in both accounts.")
                 continue

            print(f"  📍 Checking {repo_name} status...")

            # Fetch latest from mouyleng172 remote
            if not dry_run:
                print(f"  ⬇️ Fetching updates in {mouy_repo_path}")
                run_command("git fetch --all", cwd=mouy_repo_path, hide_output=True)
                run_command("git pull", cwd=mouy_repo_path, hide_output=True)

            if check_uncommitted_changes(mouy_repo_path):
                 print(f"  ⚠️ Warning: Uncommitted changes in {mouy_repo_path}. Commit before syncing.")
                 continue

            if dry_run:
                 print(f"  [DRY RUN] Would copy updates from {mouy_repo_path} to {leng_repo_path}")
            else:
                 # Real sync logic would involve pushing from one remote to another,
                 # or copying files and committing.
                 # For a simple 'Hot Melting Iron' file copy between local folders:
                 # (Excluding .git to maintain separate git histories if desired, or adding as remote)
                 print(f"  [Action Needed] Add robust sync logic here depending on desired Git history integration.")
                 print(f"  Example: Add {mouy_repo_path} as a remote to {leng_repo_path} and pull.")

                 # Adding mouyleng remote to lengkundee
                 remotes = run_command("git remote -v", cwd=leng_repo_path, hide_output=True)
                 if "mouyleng_remote" not in (remotes or ""):
                     print(f"  🔗 Adding remote 'mouyleng_remote' to {leng_repo_path}")
                     run_command(f"git remote add mouyleng_remote {mouy_repo_path}", cwd=leng_repo_path, hide_output=True)

                 print(f"  ⬇️ Fetching from mouyleng_remote...")
                 run_command("git fetch mouyleng_remote", cwd=leng_repo_path, hide_output=True)

                 # Attempting merge (might require manual conflict resolution)
                 print(f"  🔀 Merging updates...")
                 merge_result = run_command(f"git merge mouyleng_remote/main --allow-unrelated-histories -m 'Auto-sync from mouyleng172'", cwd=leng_repo_path, hide_output=True)
                 if merge_result is None:
                     print(f"  ⚠️ Merge conflict or error in {repo_name}. Manual resolution required.")
                 else:
                     print(f"  ✅ Successfully merged changes into {leng_repo_path}")
                     # Optionally push to LengKundee remote
                     # run_command("git push origin main", cwd=leng_repo_path)

if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    cross_sync(dry_run=dry_run)

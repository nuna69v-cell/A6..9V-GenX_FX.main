import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

DRIVE_PATH = os.getenv("DRIVE_PATH")
ACCOUNTS = {
    "mouyleng172": os.getenv("GH_TOKEN_MOUY"),
    "LengKundee": os.getenv("GH_TOKEN_LENG"),
}


def hot_melting_iron_sync(repo_name, remote_url):
    """Force merges and syncs repositories to the local drive."""
    print(f"🔥 Processing: {repo_name}")
    path = os.path.join(DRIVE_PATH, "Workspace", repo_name)

    if not os.path.exists(path):
        subprocess.run(["git", "clone", remote_url, path])

    os.chdir(path)
    # The 'Hot Melting Iron' Logic
    subprocess.run(["git", "fetch", "--all"])
    subprocess.run(["git", "reset", "--hard", "origin/main"])
    print(f"✅ {repo_name} is synchronized.")


if __name__ == "__main__":
    # Example execution for your main repo
    hot_melting_iron_sync("all-in-one-desktop", "https://github.com/Mouy-leng172.git")

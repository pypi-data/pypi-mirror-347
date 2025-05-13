# commit_gen/cli.py

import argparse
import subprocess
import requests
import sys
import hashlib
import json
from pathlib import Path
import socket
import uuid
import os

# Color constants for terminal output
class Colors:
    RESET = "\033[0m"
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;82m"
    YELLOW = "\033[38;5;226m"
    BLUE = "\033[38;5;33m"
    MAGENTA = "\033[38;5;207m"
    CYAN = "\033[38;5;39m"
    ORANGE = "\033[38;5;214m"

# Helper function to check if git diff is staged
def get_staged_diff():
    try:
        # Check if git is available
        subprocess.check_call(["git", "--version"])
        diff = subprocess.check_output(["git", "diff", "--cached"], stderr=subprocess.STDOUT)
        return diff.decode("utf-8")
    except subprocess.CalledProcessError:
        print(f"{Colors.RED}Error: Unable to fetch git diff (are you in a Git repository?){Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Git is not installed or not found in your PATH.{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

# Generate a unique user ID based on MAC or hostname
def generate_user_id():
    try:
        mac = hex(uuid.getnode())  # Get MAC address
        hostname = socket.gethostname()
        unique_string = f"{mac}-{hostname}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:12]
    except Exception:
        # Fallback in case MAC address can't be fetched
        home_dir = str(Path.home())
        fallback_string = f"{home_dir}-{hostname}"
        return hashlib.sha256(fallback_string.encode()).hexdigest()[:12]

# Function to generate commit message using the backend server
def generate_commit_message(server_url, diff):
    payload = {"diff": diff}
    try:
        response = requests.post(server_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("commit_message", "[No commit message returned]")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

# Run code review using the backend server
def run_code_review(server_url, user_id, diff):
    payload = {"diff": diff, "user_id": user_id}
    try:
        response = requests.post(f"{server_url}/generate-code-review", json=payload)
        response.raise_for_status()
        print(f"{Colors.GREEN}Code Review Results:{Colors.RESET}")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

# Suggest code fixes using the backend server
def suggest_code_fixes(server_url, user_id):
    payload = {"user_id": user_id, "diff": ""}  # diff not required
    try:
        response = requests.post(f"{server_url}/generate-code-fixes", json=payload)
        response.raise_for_status()
        print(f"{Colors.GREEN}Suggested Code Fixes:{Colors.RESET}")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)

def main():
    # Load server URL from environment variable if available
    server_url = os.getenv("SERVER_URL", "https://ekj89qunr6.execute-api.ap-south-1.amazonaws.com/Prod")
    
    # Command-line argument parser
    parser = argparse.ArgumentParser(description="AI commit and code review CLI")
    parser.add_argument("command", choices=["generate-commit", "run-code-review", "suggest-code-fixes"])
    parser.add_argument(
        "--server",
        type=str,
        default=server_url,
        help="Backend server base URL (default from environment or hardcoded)",
    )
    args = parser.parse_args()

    user_id = generate_user_id()

    # Refactored staged diff check to avoid repetition
    def check_staged_changes():
        diff = get_staged_diff()
        if not diff.strip():
            print(f"{Colors.YELLOW}No staged changes found. Please stage your changes (git add) before running this tool.{Colors.RESET}")
            sys.exit(1)
        return diff

    if args.command == "generate-commit":
        diff = check_staged_changes()
        commit_message = generate_commit_message(f"{args.server}/generate-commit", diff)
        print(f"{Colors.CYAN}Generated Commit Message:{Colors.RESET}")
        print(commit_message)

    elif args.command == "run-code-review":
        diff = check_staged_changes()
        run_code_review(args.server, user_id, diff)

    elif args.command == "suggest-code-fixes":
        suggest_code_fixes(args.server, user_id)

if __name__ == "__main__":
    main()

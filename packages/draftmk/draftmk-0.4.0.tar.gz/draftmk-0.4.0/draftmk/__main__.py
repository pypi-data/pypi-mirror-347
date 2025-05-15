#!/usr/bin/env python3
import argparse
import os
import random
import re
import shutil
import socket
import subprocess
import time
import urllib.request
from pathlib import Path


def check_prerequisites():
    required = ["docker", "docker-compose"]
    for cmd in required:
        if not shutil.which(cmd):
            print(
                f"[ERROR] Required command '{cmd}' not found. Please install it and try again."
            )
            exit(1)


def find_open_port(used_ports):
    while True:
        port = random.randint(3000, 3999)
        if port in used_ports:
            continue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                used_ports.add(port)
                return port
            except OSError:
                continue


def generate_env(env_path):
    used = set()
    fp = find_open_port(used)
    bp = find_open_port(used)
    pp = find_open_port(used)

    with open(env_path, "w") as f:
        f.write(f"FRONTEND_PORT={fp}\n")
        f.write(f"BACKEND_PORT={bp}\n")
        f.write(f"PREVIEW_PORT={pp}\n")
        f.write("GITHUB_TOKEN=\n")
        f.write("GITHUB_REPO=draftmk-template\n")
        f.write("GITHUB_BRANCH=main\n")
        f.write(f"VITE_API_BASE_URL=http://localhost:{bp}\n")
        f.write(f"VITE_DOCS_PREVIEW_BASE_URL=http://localhost:{pp}\n")
        f.write("VITE_ENVIRONMENT=production\n")


def init_project(target_dir="."):
    check_prerequisites()
    target = Path(target_dir)
    print(f"[INFO] Initializing DraftMk in: {target.resolve()}")
    (target / ".draftmk/config").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/site/public").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/site/internal").mkdir(parents=True, exist_ok=True)
    (target / ".draftmk/logs").mkdir(parents=True, exist_ok=True)
    generate_env(target / ".env")
    print("[INFO] .env file created.")
    print("[INFO] Directories initialized.")

    # Initialize git repo if not already a repo
    if not (target / ".git").exists():
        try:
            subprocess.run(["git", "init"], cwd=target, check=True)
            print("[INFO] Initialized a new Git repository.")
        except Exception as e:
            print(f"[WARN] Could not initialize Git repository: {e}")

    # Download docker-compose.yml if it doesn't exist
    compose_url = "https://gist.githubusercontent.com/jonmatum/5175f2de585958b6466d7b328057f62c/raw/docker-compose.yml"
    compose_file = target / "docker-compose.yml"
    if not compose_file.exists():
        print("[INFO] Downloading docker-compose.yml from GitHub Gist...")
        try:
            urllib.request.urlretrieve(compose_url, compose_file)
            print("[INFO] docker-compose.yml downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download docker-compose.yml: {e}")


def preview(open_browser=False):
    check_prerequisites()

    print("\033c", end="")  # Clear terminal screen

    print("[INFO] Pulling latest images...")
    subprocess.run(["docker-compose", "--env-file", ".env", "pull"])

    try:
        with open(".env") as f:
            lines = f.readlines()
        port = next(
            (
                line.split("=")[1].strip()
                for line in lines
                if line.startswith("FRONTEND_PORT=")
            ),
            "80",
        )
        url = f"http://localhost:{port}"
    except Exception:
        url = "http://localhost"

    print("\n DraftMk Preview is starting...")
    print(f"Access your frontend at: {url}")
    if open_browser:
        from webbrowser import open as open_url

        print("[INFO] Opening browser automatically...")
        open_url(url)

    print("[INFO] Services are starting with logs below (press Ctrl+C to stop)\n")

    subprocess.run(
        [
            "docker-compose",
            "--env-file",
            ".env",
            "up",
            "--build",
            "--remove-orphans",
            "--force-recreate",
        ]
    )


def view():
    check_prerequisites()
    if not os.path.exists(".env"):
        print(
            "[ERROR] .env file not found. Please run 'draftmk init' or 'draftmk up' first."
        )
        return
    try:
        from webbrowser import open as open_url

        with open(".env") as f:
            lines = f.readlines()
        port = next(
            (
                line.split("=")[1].strip()
                for line in lines
                if line.startswith("FRONTEND_PORT=")
            ),
            "80",
        )
        url = f"http://localhost:{port}"
        print(f"[INFO] Opening browser at {url}")
        open_url(url)
    except Exception as e:
        print(f"[WARN] Failed to open browser: {e}")


def logs():
    log_path = ".draftmk/logs/draftmk.log"
    if not os.path.exists(log_path):
        print("[INFO] No log file found yet.")
        return
    print("[INFO] Showing last 50 lines from log:")
    subprocess.run(["tail", "-n", "50", log_path])


def stop():
    check_prerequisites()
    print("[INFO] Stopping DraftMk services...")
    subprocess.run(["docker-compose", "--env-file", ".env", "down"])


def up():
    if not Path(".env").exists():
        print("[INFO] .env not found, running init...")
        init_project()
    preview(open_browser=True)


def status():
    check_prerequisites()
    print("[INFO] Checking DraftMk service status...\n")
    subprocess.run(["docker-compose", "--env-file", ".env", "ps"])


def main():
    parser = argparse.ArgumentParser(description="Draftmk CLI")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize Draftmk project")
    init_parser.add_argument("target", nargs="?", default=".", help="Target directory")

    preview_parser = subparsers.add_parser(
        "preview", help="Start Docker Compose preview"
    )
    preview_parser.add_argument(
        "--open", action="store_true", help="Open frontend in browser after start"
    )
    subparsers.add_parser("view", help="Open frontend in browser")
    subparsers.add_parser("logs", help="Show recent logs")
    subparsers.add_parser("stop", help="Stop Docker services")
    subparsers.add_parser(
        "up", help="Start Draftmk environment (init + preview + open)"
    )
    subparsers.add_parser("status", help="Show status of Draftmk services")

    args = parser.parse_args()

    if args.command == "init":
        target = args.target
        if target == ".":
            target = (
                input(
                    "Enter a project directory name (e.g., my-docs) [default: draftmk-docs]: "
                ).strip()
                or "draftmk-docs"
            )

        if not re.match(r"^[a-z]+(-[a-z]+)*$", target):
            print(
                "[ERROR] Invalid project name. Use lowercase letters and hyphens only (e.g., draftmk-docs)."
            )
            return

        init_project(target)
        print(f"[INFO] To get started:\n  cd {target}\n  draftmk up")
    elif args.command == "preview":
        preview(open_browser=args.open)
    elif args.command == "view":
        view()
    elif args.command == "logs":
        logs()
    elif args.command == "stop":
        stop()
    elif args.command == "up":
        up()
    elif args.command == "status":
        status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

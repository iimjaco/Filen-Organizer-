import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# ===============================================================
# File Organizer - Configurable Version
# Author: Jacopo Marcon
# Description:
#   This script organizes files into subfolders based on extensions.
#   Configuration (folders, extensions, source path) is loaded from
#   an external config.json file.
# ===============================================================

# Paths
CONFIG_FILE = Path(__file__).parent / "config.json"

LOG_FILE = Path("organizer_log.txt")

print("Current working directory:", os.getcwd())
print("Looking for config.json at:", CONFIG_FILE.resolve())



def load_config():
    """Load configuration settings from config.json."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def log_action(message: str):
    """Append a log message with timestamp to the log file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now()}] {message}\n")


def organize_files(source_dir: Path, folders: dict):
    """Organize files from the source directory according to config."""
    if not source_dir.exists():
        print(f"⚠️ Source folder not found: {source_dir}")
        log_action(f"ERROR: Source folder not found: {source_dir}")
        return

    for file in source_dir.iterdir():
        if file.is_file():
            moved = False
            for folder, extensions in folders.items():
                if file.suffix.lower() in extensions:
                    try:
                        target_dir = source_dir / folder
                        target_dir.mkdir(exist_ok=True)
                        shutil.move(str(file), str(target_dir / file.name))
                        print(f"📂 Moved {file.name} -> {folder}")
                        log_action(f"Moved {file.name} -> {folder}")
                        moved = True
                        break
                    except Exception as e:
                        print(f"❌ Error moving {file.name}: {e}")
                        log_action(f"ERROR: {file.name} -> {e}")

            if not moved:
                try:
                    target_dir = source_dir / "Others"
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))
                    print(f"📂 Moved {file.name} -> Others")
                    log_action(f"Moved {file.name} -> Others")
                except Exception as e:
                    print(f"❌ Error moving {file.name}: {e}")
                    log_action(f"ERROR: {file.name} -> {e}")


if __name__ == "__main__":
    print("=== File Organizer Started ===")
    log_action("=== File Organizer Started ===")

    # Load configuration
    try:
        config = load_config()
        source_dir = Path(config["source_directory"])
        folders = config["folders"]
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        log_action(f"ERROR: Failed to load config -> {e}")
        exit(1)

    # Run organizer
    print("Scanning folder:", source_dir)
    organize_files(source_dir, folders)

    print("✅ Organization completed. See organizer_log.txt for details.")
    log_action("Organization completed.")

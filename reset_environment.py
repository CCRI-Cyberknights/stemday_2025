#!/usr/bin/env python3
import os
import shutil
import fnmatch
from pathlib import Path

# Configuration
GITIGNORE_PATH = ".gitignore"
TARGET_DIRS = ["challenges", "challenges_solo"]
FIREFOX_DIR = Path.home() / ".mozilla" / "firefox"

def load_gitignore_rules(gitignore_path):
    """
    Parses .gitignore into a list of rules.
    Returns list of tuples: (is_whitelist, pattern)
    """
    rules = []
    if not os.path.exists(gitignore_path):
        print(f"⚠️ Warning: {gitignore_path} not found. Using default unsafe mode (Delete All).")
        return []

    with open(gitignore_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            is_whitelist = False
            pattern = line
            
            if line.startswith("!"):
                is_whitelist = True
                pattern = line[1:]
            
            # Normalization for fnmatch
            if pattern.startswith("/"):
                pattern = pattern[1:]
            
            rules.append((is_whitelist, pattern))
    return rules

def should_keep_file(rel_path, rules):
    """
    Determines if a file should be kept based on gitignore logic.
    Logic: Iterate ALL rules. Last match wins.
    """
    keep = False # Default to 'Ignore/Delete' because of the '*' rule
    
    for is_whitelist, pattern in rules:
        # Check against the pattern (and implied wildcards for directory matches)
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(rel_path, f"*{pattern}"):
            keep = is_whitelist
            
    return keep

def clean_directory(base_dir, rules):
    """
    Walks the directory and deletes files that are not whitelisted.
    """
    # FIX: Resolve to absolute path so os.walk yields absolute paths
    base_path = Path(base_dir).resolve()
    
    if not base_path.exists():
        print(f"⚠️ Directory not found: {base_dir}")
        return

    print(f"🧹 Cleaning: {base_dir}...")
    
    for root, dirs, files in os.walk(base_path):
        for name in files:
            file_path = Path(root) / name
            
            # Both paths are now absolute, so relative_to works correctly
            try:
                rel_path = file_path.relative_to(Path.cwd()).as_posix()
            except ValueError:
                # This happens if the file is somehow outside the project root
                continue
            
            # Check if we should keep this file
            if should_keep_file(rel_path, rules):
                # It's a whitelisted file (e.g. README.md, squirrel.jpg)
                continue
            else:
                # It's trash (flag.txt, .solver.py, etc)
                try:
                    os.remove(file_path)
                    print(f"   🗑️  Deleted: {rel_path}")
                except Exception as e:
                    print(f"   ❌ Error deleting {rel_path}: {e}")

def reset_firefox():
    """
    Clears Firefox history/cookies by removing the storage and profile data 
    but keeping the profile folder structure itself.
    """
    print("🦊 Resetting Firefox data...")
    if not FIREFOX_DIR.exists():
        print("   ⚠️ Firefox directory not found. Skipping.")
        return

    # We want to clear specific data files inside the profiles
    for profile in FIREFOX_DIR.glob("*.default-release"):
        print(f"   Cleaning profile: {profile.name}")
        
        # Files to nuke for a "fresh" feel without breaking the browser
        targets = [
            "cookies.sqlite", "places.sqlite", "formhistory.sqlite", 
            "key4.db", "logins.json", "sessionstore.jsonlz4", "webappsstore.sqlite",
            "storage", "cache2", "startupCache"
        ]
        
        for target in targets:
            target_path = profile / target
            try:
                if target_path.is_file():
                    os.remove(target_path)
                elif target_path.is_dir():
                    shutil.rmtree(target_path)
            except Exception:
                pass
                
    print("   ✅ Firefox data cleared.")

def main():
    print("==========================================")
    print("      🔄 ENVIRONMENT RESET SCRIPT")
    print("==========================================\n")
    
    # 1. Parse Rules
    rules = load_gitignore_rules(GITIGNORE_PATH)
    
    # 2. Clean Challenge Directories
    for target in TARGET_DIRS:
        clean_directory(target, rules)
        
    # 3. Reset Firefox
    reset_firefox()
    
    print("\n✨ Reset Complete. Environment is ready for the next student.")

if __name__ == "__main__":
    main()
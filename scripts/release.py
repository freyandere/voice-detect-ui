#!/usr/bin/env python3
"""Release script for voice-detect-ui.

Reads version from pyproject.toml, parses Conventional Commits since last tag,
generates changelog, bumps version, commits, tags, and pushes.
"""

import subprocess
import re
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path("E:/2.Projects/voice-detect-ui")
PYPROJECT = PROJECT_ROOT / "pyproject.toml"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"

def get_version():
    with open(PYPROJECT) as f:
        match = re.search(r'version\s*=\s*"([^"]+)"', f.read())
        if not match:
            raise ValueError("Cannot find version in pyproject.toml")
        return match.group(1)

def get_last_tag():
    result = subprocess.run(["git", "tag", "--sort=-version:refname"], capture_output=True, text=True, cwd=PROJECT_ROOT)
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.strip().split("\n")[0]

def get_conventional_commits():
    last_tag = get_last_tag()
    if not last_tag:
        result = subprocess.run(["git", "log", "--oneline"], capture_output=True, text=True, cwd=PROJECT_ROOT)
        return result.stdout.strip().split("\n") if result.returncode == 0 else []
    
    result = subprocess.run(["git", "log", f"{last_tag}..HEAD", "--oneline", "--no-decorate"], capture_output=True, text=True, cwd=PROJECT_ROOT)
    return result.stdout.strip().split("\n") if result.returncode == 0 else []

def generate_changelog(commits):
    if not commits:
        return ""
    
    lines = []
    for commit in commits:
        if "ci:" in commit:
            continue
        if commit.startswith("initial"):
            continue
        lines.append(f"- {commit}")
    
    if not lines:
        return ""
    
    return "\n".join(lines)

def bump_version(version, bump_type):
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def update_pyproject(new_version):
    with open(PYPROJECT) as f:
        content = f.read()
    
    content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
    
    with open(PYPROJECT, 'w') as f:
        f.write(content)

def update_changelog(new_version, changelog_entries):
    if not changelog_entries:
        return
    
    with open(CHANGELOG) as f:
        content = f.read()
    
    new_section = f"\n## v{new_version}\n{changelog_entries}\n"
    
    if f"## v{new_version}" in content:
        print(f"Version v{new_version} already exists in CHANGELOG. Skipping duplicate.")
        return
    
    content = new_section + "\n" + content
    
    with open(CHANGELOG, 'w') as f:
        f.write(content)

def commit_and_tag(version):
    subprocess.run(["git", "add", "pyproject.toml", "CHANGELOG.md"], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "commit", "-m", f"release: v{version}"], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "tag", "-a", f"v{version}", "-m", f"Version v{version}"], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "push", "--tags"], cwd=PROJECT_ROOT, check=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: release.py [--dry-run] --bump [patch|minor|major] [--publish]")
        sys.exit(1)
    
    dry_run = "--dry-run" in sys.argv
    bump_type = None
    publish = False
    
    for i, arg in enumerate(sys.argv):
        if arg == "--bump" and i + 1 < len(sys.argv):
            bump_type = sys.argv[i + 1]
        if arg == "--publish":
            publish = True
    
    if not bump_type:
        print("Missing --bump argument")
        sys.exit(1)
    
    if bump_type not in ["patch", "minor", "major"]:
        print("Invalid bump type")
        sys.exit(1)
    
    current_version = get_version()
    new_version = bump_version(current_version, bump_type)
    
    print(f"Current version: {current_version}")
    print(f"New version: {new_version}")
    
    commits = get_conventional_commits()
    changelog_entries = generate_changelog(commits)
    
    print(f"\nChangelog entries ({len(commits)} commits):")
    for commit in commits:
        print(f"  - {commit}")
    
    if dry_run:
        print("\n=== DRY RUN ===")
        print(f"Would bump version to {new_version}")
        print(f"Would update pyproject.toml")
        print(f"Would update CHANGELOG.md")
        print(f"Would commit and tag v{new_version}")
        return
    
    update_pyproject(new_version)
    update_changelog(new_version, changelog_entries)
    
    print("\n=== COMMITTING ===")
    commit_and_tag(new_version)
    
    print(f"\n✅ Release v{new_version} complete!")
    if publish:
        print("Pushed tags to GitHub.")

if __name__ == "__main__":
    main()

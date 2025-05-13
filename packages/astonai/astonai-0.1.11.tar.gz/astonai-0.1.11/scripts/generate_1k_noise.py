#!/usr/bin/env python3
"""
Generate 1000 Lines of Noise for Benchmark Testing (Simple Version)

This script adds approximately 1000 lines of comments to django/__init__.py
for benchmarking purposes. This is a simplified approach to ensure we get
exactly the number of lines we want.

Usage:
    python scripts/generate_1k_noise_simple.py <django_repo_path> [lines]

Example:
    python scripts/generate_1k_noise_simple.py bench_repo 1000
"""

import os
import sys
import subprocess
from pathlib import Path

def generate_changes(repo_path, target_lines=1000):
    """Generate approximately target_lines of changes in the repository."""
    repo_root = Path(repo_path)
    init_py = repo_root / "django" / "__init__.py"
    
    if not init_py.exists():
        print(f"Error: File {init_py} not found")
        return False
    
    print(f"Adding {target_lines} noise lines to {init_py.relative_to(repo_root)}")
    with open(init_py, 'a') as f:
        f.write("\n# BEGIN BENCHMARK NOISE\n")
        for i in range(target_lines):
            f.write(f"# BENCHMARK_NOISE_LINE_{i:04d}: This line was added for benchmarking purposes\n")
        f.write("# END BENCHMARK NOISE\n")
    
    # Check how many lines were changed
    git_status = subprocess.run(
        ["git", "diff", "--numstat"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    
    total_additions = 0
    total_deletions = 0
    
    for line in git_status.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            additions = int(parts[0])
            deletions = int(parts[1])
            total_additions += additions
            total_deletions += deletions
    
    print(f"Generated changes: {total_additions} additions, {total_deletions} deletions")
    print(f"Total lines changed: {total_additions + total_deletions}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <django_repo_path> [lines]")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    target_lines = 1000
    
    if len(sys.argv) > 2:
        try:
            target_lines = int(sys.argv[2])
        except ValueError:
            print(f"Error: Lines argument must be an integer, got {sys.argv[2]}")
            sys.exit(1)
    
    if not os.path.isdir(repo_path):
        print(f"Error: Repository path {repo_path} not found or is not a directory")
        sys.exit(1)
    
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Warning: {repo_path} does not appear to be a git repository")
    
    if generate_changes(repo_path, target_lines):
        print("Successfully generated noise for benchmark testing")
    else:
        print("Failed to generate sufficient changes")
        sys.exit(1)

if __name__ == "__main__":
    main() 
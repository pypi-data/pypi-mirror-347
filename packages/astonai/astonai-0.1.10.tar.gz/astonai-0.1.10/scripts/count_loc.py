#!/usr/bin/env python3
"""
Count Lines of Code

This utility script counts:
1. The number of added and removed lines in a diff file
2. The number of lines of Python code in a directory

Usage:
    python scripts/count_loc.py <diff_file_or_directory>

Examples:
    python scripts/count_loc.py patches/django_1k.diff
    python scripts/count_loc.py bench_repo/
"""

import sys
import os
import glob
from pathlib import Path

def count_diff_lines(diff_file):
    """Count added and removed lines in a diff file."""
    if not os.path.exists(diff_file):
        print(f"Error: File not found: {diff_file}")
        return None
    
    added_lines = 0
    removed_lines = 0
    
    with open(diff_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('+') and not line.startswith('+++'):
                added_lines += 1
            elif line.startswith('-') and not line.startswith('---'):
                removed_lines += 1
    
    return {
        'added': added_lines,
        'removed': removed_lines,
        'total_changes': added_lines + removed_lines,
        'net_change': added_lines - removed_lines
    }

def count_python_lines(directory):
    """Count lines of Python code in a directory."""
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return 0
    
    total_lines = 0
    python_files = []
    
    # Recursively find all Python files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Count lines in each Python file
    for python_file in python_files:
        with open(python_file, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                lines = f.readlines()
                total_lines += len(lines)
            except UnicodeDecodeError:
                print(f"Warning: Could not read file: {python_file}")
    
    return total_lines

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <diff_file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Check if the target is a directory
    if os.path.isdir(target):
        line_count = count_python_lines(target)
        print(line_count)  # Just output the number for easy parsing
        return
    
    # Otherwise, treat it as a diff file
    counts = count_diff_lines(target)
    
    if counts:
        print(f"Lines of code in {target}:")
        print(f"  Added lines:    {counts['added']}")
        print(f"  Removed lines:  {counts['removed']}")
        print(f"  Total changes:  {counts['total_changes']}")
        print(f"  Net change:     {counts['net_change']}")
        
        # Provide guidance for benchmark patches
        if target.endswith('_1k.diff') and abs(counts['total_changes'] - 1000) > 100:
            print(f"\nWarning: Total changes ({counts['total_changes']}) differs significantly from 1000 LOC target.")
            print("Consider adjusting the patch to be closer to 1000 lines of changes for benchmark consistency.")

if __name__ == "__main__":
    main() 
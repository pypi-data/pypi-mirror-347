#!/usr/bin/env python3
"""
Generate Realistic 1000 LOC Diff for Benchmark Testing

This script creates a realistic diff by making these types of changes:
1. Adding new functions
2. Renaming existing functions
3. Inserting function calls
4. Tweaking constants 

The changes are spread across multiple files to better simulate real-world code changes.

Usage:
    python scripts/generate_realistic_diff.py --repo <repo_path> --files-per-patch <num> --loc-per-file <num>

Example:
    python scripts/generate_realistic_diff.py --repo bench_repo --files-per-patch 10 --loc-per-file 100
"""

import os
import sys
import re
import random
import argparse
import subprocess
from pathlib import Path
import fnmatch

def find_py_files(repo_path, max_files=20):
    """Find Python files in the repository."""
    result = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                # Only include files from the Django core
                if 'django' in root:
                    file_path = os.path.join(root, file)
                    result.append(file_path)
                    if len(result) >= max_files:
                        return result
    return result

def add_dummy_function(file_path, idx):
    """Add a new dummy function to a file."""
    lines_added = 0
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Generate a random function with docstring and some code
    func_name = f"__benchmark_dummy_{idx}"
    func_lines = [
        f"\n\ndef {func_name}(x, y=None, z=10):",
        f"    '''",
        f"    Benchmark dummy function {idx}",
        f"    ",
        f"    Args:",
        f"        x: Primary parameter",
        f"        y: Optional secondary parameter",
        f"        z: Third parameter with default value",
        f"    ",
        f"    Returns:",
        f"        Processed value",
        f"    '''",
        f"    result = x * {idx}",
        f"    if y is not None:",
        f"        result += y * {idx % 5}",
        f"    return result + z"
    ]
    
    # Append to the end of the file
    with open(file_path, 'a') as f:
        for line in func_lines:
            f.write(line + '\n')
    
    return len(func_lines)

def rename_function(file_path):
    """Rename a function in the file and update all references."""
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    # Find function definitions
    functions = []
    for i, line in enumerate(content):
        match = re.match(r'^\s*def\s+(\w+)\s*\(', line)
        if match and not match.group(1).startswith('__'):
            functions.append((i, match.group(1)))
    
    if not functions:
        return 0
    
    # Select a random function to rename
    line_num, old_name = random.choice(functions)
    new_name = f"{old_name}_benchmarked"
    
    # Rename the function and all its references
    lines_changed = 0
    
    for i, line in enumerate(content):
        if re.search(r'\b' + re.escape(old_name) + r'\b', line):
            content[i] = line.replace(old_name, new_name)
            lines_changed += 1
    
    with open(file_path, 'w') as f:
        f.writelines(content)
    
    return lines_changed

def modify_constants(file_path):
    """Find and modify constants in the file."""
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    # Find constant-like assignments
    constants = []
    for i, line in enumerate(content):
        match = re.match(r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*(\d+)', line)
        if match:
            constants.append((i, match.group(1), int(match.group(2))))
    
    if not constants:
        return 0
    
    # Select a random constant to modify
    lines_changed = 0
    modified_lines = set()
    
    # Modify up to 3 constants
    for _ in range(min(3, len(constants))):
        if not constants:
            break
            
        idx = random.randint(0, len(constants) - 1)
        line_num, name, value = constants.pop(idx)
        
        if line_num in modified_lines:
            continue
            
        # Modify the value slightly
        new_value = value + random.randint(1, 5)
        content[line_num] = re.sub(r'(\s*' + re.escape(name) + r'\s*=\s*)\d+', 
                                   r'\g<1>' + str(new_value), 
                                   content[line_num])
        lines_changed += 1
        modified_lines.add(line_num)
    
    with open(file_path, 'w') as f:
        f.writelines(content)
    
    return lines_changed

def insert_function_call(file_path):
    """Insert a function call somewhere in the file."""
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    # Find possible insertion points (inside functions)
    insertion_points = []
    inside_func = False
    func_indent = 0
    current_func = ""
    
    for i, line in enumerate(content):
        if not inside_func:
            match = re.match(r'^(\s*)def\s+(\w+)\s*\(', line)
            if match:
                inside_func = True
                func_indent = len(match.group(1))
                current_func = match.group(2)
        else:
            # Check if we're still inside the function
            if line.strip() and not line.isspace():
                indent = len(line) - len(line.lstrip())
                if indent <= func_indent:
                    inside_func = False
                else:
                    # This is a good insertion point
                    insertion_points.append((i, indent, current_func))
    
    if not insertion_points:
        return 0
    
    # Select a random insertion point
    line_num, indent, func_name = random.choice(insertion_points)
    
    # Create a benchmark comment and assertion
    call_lines = [
        ' ' * indent + f"# BENCHMARK: Added function call for testing",
        ' ' * indent + f"benchmark_value = {func_name}('test') if callable({func_name}) else 0"
    ]
    
    # Insert the lines
    for i, line in enumerate(call_lines):
        content.insert(line_num + i, line + '\n')
    
    with open(file_path, 'w') as f:
        f.writelines(content)
    
    return len(call_lines)

def generate_changes(repo_path, files_per_patch=10, loc_per_file=100):
    """Generate approximately loc_per_file changes across files_per_patch files."""
    total_files = 0
    total_lines = 0
    
    # Find Python files to modify
    py_files = find_py_files(repo_path, max_files=files_per_patch * 2)
    if not py_files:
        print(f"Error: No suitable Python files found in {repo_path}")
        return False
    
    # Randomly select files to modify
    random.shuffle(py_files)
    files_to_modify = py_files[:files_per_patch]
    
    for i, file_path in enumerate(files_to_modify):
        rel_path = os.path.relpath(file_path, repo_path)
        print(f"Modifying {rel_path}...")
        
        # Determine modifications for this file
        remaining_loc = loc_per_file // files_per_patch
        
        # Add new function (approx 15 lines)
        if remaining_loc > 15:
            lines = add_dummy_function(file_path, i)
            total_lines += lines
            remaining_loc -= lines
            
        # Rename function and references (variable number of lines)
        if remaining_loc > 5:
            lines = rename_function(file_path)
            total_lines += lines
            remaining_loc -= lines
            
        # Modify constants (1-3 lines)
        if remaining_loc > 3:
            lines = modify_constants(file_path)
            total_lines += lines
            remaining_loc -= lines
            
        # Insert function call (2 lines)
        if remaining_loc > 2:
            lines = insert_function_call(file_path)
            total_lines += lines
            remaining_loc -= lines
        
        total_files += 1
    
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
    
    print(f"Generated changes across {total_files} files:")
    print(f"  - {total_lines} direct code modifications")
    print(f"  - {total_additions} additions, {total_deletions} deletions")
    print(f"  - Total lines changed: {total_additions + total_deletions}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate realistic diff for benchmark testing")
    parser.add_argument("--repo", required=True, help="Path to Django repository")
    parser.add_argument("--files-per-patch", type=int, default=10, help="Number of files to modify")
    parser.add_argument("--loc-per-file", type=int, default=100, help="Target lines of code per file")
    parser.add_argument("--output", default="patches/django_1k.diff", help="Output diff file")
    args = parser.parse_args()
    
    if not os.path.isdir(args.repo):
        print(f"Error: Repository path {args.repo} not found or is not a directory")
        sys.exit(1)
    
    if not os.path.isdir(os.path.join(args.repo, ".git")):
        print(f"Warning: {args.repo} does not appear to be a git repository")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    if generate_changes(args.repo, args.files_per_patch, args.loc_per_file):
        # Generate diff file
        try:
            diff_result = subprocess.run(
                ["git", "diff"],
                cwd=args.repo,
                capture_output=True,
                text=True,
                check=True
            )
            
            with open(args.output, 'w') as f:
                f.write(diff_result.stdout)
            
            print(f"Successfully generated realistic diff at {args.output}")
        except subprocess.CalledProcessError as e:
            print(f"Error generating diff: {e}")
            sys.exit(1)
    else:
        print("Failed to generate sufficient changes")
        sys.exit(1)

if __name__ == "__main__":
    main() 
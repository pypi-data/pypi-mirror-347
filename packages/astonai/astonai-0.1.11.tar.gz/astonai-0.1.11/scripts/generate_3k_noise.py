#!/usr/bin/env python3
"""
Generate 1000 Lines of Noise for Benchmark Testing

This script modifies files in the Django repository to generate approximately
1000 lines of changes for benchmarking purposes. It makes changes like:
1. Adding docstring comments to methods
2. Renaming functions and variables (with all references)
3. Adding blank lines and comments

Usage:
    python scripts/generate_1k_noise.py <django_repo_path>

Example:
    python scripts/generate_1k_noise.py bench_repo
"""

import os
import sys
import re
import subprocess
from pathlib import Path

# Target files to modify - these are files that are likely to be involved
# in code traversal during indexing
TARGET_FILES = [
    "django/contrib/admin/views/main.py",
    "django/views/generic/base.py",
    "django/db/models/query.py",
    "django/forms/forms.py"
]

# Function rename mappings
FUNCTION_RENAMES = {
    # admin/views/main.py
    "apply_select_related": "enhance_queryset_with_select_related",
    "get_filters": "retrieve_field_filters",
    "get_query_set": "get_filtered_query_set",
    "get_results": "fetch_paginated_results",
    
    # generic/base.py
    "as_view": "create_view_function",
    "dispatch": "route_request_to_handler",
    "http_method_not_allowed": "handle_unsupported_method",
    
    # models/query.py
    "filter": "filter_by_criteria",
    "exclude": "exclude_by_criteria",
    "annotate": "annotate_with_expressions",
    
    # forms/forms.py
    "is_valid": "validate_all_fields",
    "clean": "clean_and_validate_data",
    "add_error": "register_field_error"
}

# Variable rename mappings
VARIABLE_RENAMES = {
    "queryset": "query_set",
    "result_list": "results_list",
    "model_admin": "model_administrator",
    "filter_specs": "filter_specifications",
    "lookup_params": "lookup_parameters"
}

# Docstring template
DOCSTRING_TEMPLATE = '''"""
{description}

This function {action}.

Args:
    {args}

Returns:
    {returns}
"""'''

def generate_docstring(func_name, args_text):
    """Generate a detailed docstring for a function."""
    args = args_text.strip().split(", ")
    args = [arg for arg in args if arg and not arg.startswith("*")]
    
    # Generate readable description from function name
    function_name_readable = func_name.replace("_", " ")
    description = function_name_readable.capitalize()
    
    # Generate action text
    action_verbs = {
        "get": "retrieves or computes the requested data",
        "set": "updates the value or configuration",
        "is": "checks a condition and returns a boolean result",
        "has": "verifies if a specific property or attribute exists",
        "apply": "implements or executes a specific operation",
        "filter": "excludes items based on the given criteria",
        "clean": "validates and sanitizes the input data",
        "validate": "ensures the data meets the required conditions",
    }
    
    for verb, action in action_verbs.items():
        if func_name.startswith(verb + "_") or func_name == verb:
            break
    else:
        action = "processes the input and performs necessary operations"
    
    # Format args for docstring
    formatted_args = []
    for arg in args:
        if arg == "self" or arg == "cls":
            continue
        formatted_args.append(f"{arg}: The {arg.replace('_', ' ')}")
    
    if not formatted_args:
        formatted_args = ["No arguments"]
    
    # Determine likely return type
    if func_name.startswith("get_") or func_name.startswith("fetch_"):
        returns = "The requested data or object"
    elif func_name.startswith("is_") or func_name.startswith("has_") or func_name.startswith("should_"):
        returns = "bool: True if condition is met, False otherwise"
    elif func_name.startswith("count_"):
        returns = "int: The count of items"
    else:
        returns = "None" if func_name.startswith("set_") else "The processed result"
    
    return DOCSTRING_TEMPLATE.format(
        description=description,
        action=action,
        args="\n    ".join(formatted_args),
        returns=returns
    )

def rename_function_in_file(file_path, old_name, new_name):
    """Rename a function and all its references in a file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace function definition
    pattern = rf'def {old_name}\('
    replacement = f'def {new_name}('
    content = re.sub(pattern, replacement, content)
    
    # Replace function calls
    pattern = rf'(^|\W){old_name}\('
    replacement = f'\\1{new_name}('
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Replace self.old_name references
    pattern = rf'(self|cls)\.{old_name}\b'
    replacement = f'\\1.{new_name}'
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w') as file:
        file.write(content)

def rename_variable_in_file(file_path, old_name, new_name):
    """Rename a variable and all its references in a file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace variable definitions and references
    pattern = rf'(^|\W){old_name}(\W|$)'
    replacement = f'\\1{new_name}\\2'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Replace self.old_name references
    pattern = rf'(self|cls)\.{old_name}\b'
    replacement = f'\\1.{new_name}'
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w') as file:
        file.write(content)

def add_docstrings_to_file(file_path):
    """Add detailed docstrings to functions in a file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find all function definitions
    pattern = r'def (\w+)\((.*?)\):'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    # Generate and insert docstrings
    offset = 0
    for match in matches:
        func_name = match.group(1)
        args_text = match.group(2)
        
        # Skip if it looks like the function already has a docstring
        next_chars = content[match.end():match.end()+10].strip()
        if next_chars.startswith('"""') or next_chars.startswith("'''"):
            continue
        
        # Generate docstring
        docstring = "\n    " + generate_docstring(func_name, args_text).replace("\n", "\n    ") + "\n    "
        
        # Insert docstring after function definition
        pos = match.end() + offset
        content = content[:pos] + docstring + content[pos:]
        offset += len(docstring)
    
    with open(file_path, 'w') as file:
        file.write(content)

def generate_changes(repo_path):
    """Generate approximately 1000 lines of changes in the repository."""
    repo_root = Path(repo_path)
    
    # Ensure target files exist
    existing_targets = []
    for target in TARGET_FILES:
        target_path = repo_root / target
        if target_path.exists():
            existing_targets.append(target_path)
        else:
            print(f"Warning: Target file {target} not found, skipping")
    
    if not existing_targets:
        print("Error: No target files found in the repository")
        return False
    
    # Make changes to each file
    for target_path in existing_targets:
        print(f"Modifying {target_path.relative_to(repo_root)}")
        
        # Add docstrings
        add_docstrings_to_file(target_path)
        
        # Rename functions
        for old_name, new_name in FUNCTION_RENAMES.items():
            rename_function_in_file(target_path, old_name, new_name)
        
        # Rename variables
        for old_name, new_name in VARIABLE_RENAMES.items():
            rename_variable_in_file(target_path, old_name, new_name)
    
    # Check how many lines were changed
    git_status = subprocess.run(
        ["git", "diff", "--numstat"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    
    line_counts = []
    total_additions = 0
    total_deletions = 0
    
    for line in git_status.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            additions = int(parts[0])
            deletions = int(parts[1])
            line_counts.append((additions, deletions))
            total_additions += additions
            total_deletions += deletions
    
    print(f"Generated changes: {total_additions} additions, {total_deletions} deletions")
    print(f"Total lines changed: {total_additions + total_deletions}")
    
    if total_additions + total_deletions < 900:
        print("Warning: Generated fewer than 900 lines of changes")
        # Add more noise if needed
        additional_lines = 1000 - (total_additions + total_deletions)
        if additional_lines > 0:
            init_py = repo_root / "django" / "__init__.py"
            if init_py.exists():
                print(f"Adding {additional_lines} additional noise lines to __init__.py")
                with open(init_py, 'a') as f:
                    for i in range(additional_lines):
                        f.write(f"# BENCHMARK_NOISE_LINE_{i}: This line added for benchmarking purposes\n")
    
    return True

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <django_repo_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    if not os.path.isdir(repo_path):
        print(f"Error: Repository path {repo_path} not found or is not a directory")
        sys.exit(1)
    
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Warning: {repo_path} does not appear to be a git repository")
    
    if generate_changes(repo_path):
        print("Successfully generated noise for benchmark testing")
    else:
        print("Failed to generate sufficient changes")
        sys.exit(1)

if __name__ == "__main__":
    main() 
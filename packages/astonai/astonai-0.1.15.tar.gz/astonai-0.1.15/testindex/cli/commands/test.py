"""
TestIndex test command.

This module implements the `testindex test` command that runs tests with coverage.
"""
import os
import subprocess
import sys
import re
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console

from testindex.core.cli.runner import common_options
from testindex.core.logging import get_logger
from testindex.core.exceptions import CLIError

# Set up logger
logger = get_logger(__name__)


@click.command('test', help='Run tests with coverage')
@click.option('--pytest-args', type=str, help='Additional arguments to pass to pytest')
@click.option('--no-cov', is_flag=True, help='Run tests without coverage')
@click.option('--verbose', is_flag=True, help='Show detailed output')
@click.option('--summary-only', is_flag=True, help='Show only summary')
@common_options
def test_command(pytest_args: Optional[str], no_cov: bool = False, verbose: bool = False, summary_only: bool = False, **kwargs):
    """Run tests with coverage.
    
    This command:
    1. Runs pytest with coverage
    2. Generates coverage.xml file in the repository root
    
    Exit codes:
    - 0: Tests passed
    - 1: Tests failed
    - 2: Other error occurred
    """
    try:
        console = Console()
        
        # Check Python version
        python_version = sys.version.split()[0]
        
        if not summary_only:
            console.print(f"🧪 Running tests with coverage...")
            console.print(f"🐍 Test runner: pytest (Python {python_version})")
        
        # Use the repository root (current directory) for coverage output
        output_dir = Path.cwd()
        
        # Run pytest with or without coverage
        if no_cov:
            cmd = ["python", "-m", "pytest"]
        else:
            cmd = [
                "python", "-m", "pytest",
                "--cov", ".",
                "--cov-report", f"xml:{output_dir / 'coverage.xml'}",
            ]
        
        # Add user-provided pytest args if specified
        if pytest_args:
            cmd.extend(pytest_args.split())
        
        # Add quiet mode if summary_only is specified
        if summary_only and "--quiet" not in cmd and "-q" not in cmd:
            cmd.append("-q")
        
        if verbose:
            logger.info(f"Running: {' '.join(cmd)}")
        
        # Run the pytest command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Extract test stats if summary_only mode
        if summary_only:
            # Just show the summary line
            summary_lines = [line for line in result.stdout.splitlines() if " passed, " in line]
            if summary_lines:
                console.print(summary_lines[-1])
            else:
                console.print(result.stdout)
        else:
            # Print full output
            console.print(result.stdout)
            
            # Extract test stats from output to show in a nicely formatted way
            collected_match = re.search(r'collected (\d+) items', result.stdout)
            if collected_match:
                test_count = collected_match.group(1)
                console.print(f"✅ Collected {test_count} tests")
            
            passed_match = re.search(r'(\d+) passed', result.stdout)
            failed_match = re.search(r'(\d+) failed', result.stdout)
            skipped_match = re.search(r'(\d+) skipped', result.stdout)
            
            status_parts = []
            if passed_match:
                status_parts.append(f"Passed: {passed_match.group(1)}")
            if failed_match:
                status_parts.append(f"Failed: {failed_match.group(1)}")
            if skipped_match:
                status_parts.append(f"Skipped: {skipped_match.group(1)}")
            
            if status_parts:
                console.print(f"✅ {', '.join(status_parts)}")
            
            if not no_cov:
                console.print(f"📄 Coverage written to coverage.xml")
        
        # Check for common errors in stderr
        if result.stderr:
            if not summary_only:
                console.print("[yellow]STDERR:[/]")
                console.print(result.stderr)
            
            # Check for common errors
            if "ModuleNotFoundError: No module named 'pytest_cov" in result.stderr:
                console.print("[bold red]Error:[/] pytest-cov plugin missing")
                console.print("[bold green]Solution:[/] Run 'pip install pytest-cov' or add --no-cov flag.")
            elif "No tests were collected" in result.stderr or "No tests were collected" in result.stdout:
                console.print("[bold yellow]Warning:[/] No tests were found")
                console.print("[bold green]Hint:[/] Check if your tests are in a 'tests/' directory or named with 'test_' prefix.")
                if "Django" in result.stdout or "Django" in result.stderr:
                    console.print("[bold green]Django projects:[/] Try running 'python manage.py test' instead.")
        
        # Return appropriate exit code
        return result.returncode
        
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Error running tests:[/] {e}")
        return 2 
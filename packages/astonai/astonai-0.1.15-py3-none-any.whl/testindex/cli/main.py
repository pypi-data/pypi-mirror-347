"""
Main CLI module for TestIndex.

This module defines the main CLI command group and entry point function.
"""
import os
import sys
from typing import List, Optional

import click

from testindex.core.cli.runner import create_cli, run_cli, common_options
from testindex.core.exceptions import CLIError

# Import commands
from testindex.cli.commands.init import init_command
from testindex.cli.commands.coverage import coverage_command
from testindex.cli.commands.ingest_coverage import ingest_coverage_command
from testindex.cli.commands.test import test_command

# Create main CLI group
cli = create_cli(
    name="aston",
    help_text=(
        "Aston — build the knowledge graph for your repo and spot test‑coverage gaps.\n\n"
        "Quick‑start:\n"
        "  aston init --offline           # index the current repository\n"
        "  pytest --cov -q                # run your tests with coverage (or 'aston test')\n"
        "  aston coverage                 # see an interactive gap table\n\n"
        "Run any command with -h/--help for more options."
    ),
)

# Register commands
cli.add_command(init_command)
cli.add_command(coverage_command)
cli.add_command(ingest_coverage_command)
cli.add_command(test_command)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the TestIndex CLI.
    
    Args:
        args: Command-line arguments (default: sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Set VERBOSE environment variable if --verbose flag is used
    if args and '--verbose' in args:
        os.environ['VERBOSE'] = '1'
    
    try:
        run_cli(cli, args=args)
        return 0
    except CLIError as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        return 2

if __name__ == "__main__":
    sys.exit(main()) 
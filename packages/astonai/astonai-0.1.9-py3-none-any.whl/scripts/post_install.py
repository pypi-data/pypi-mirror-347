#!/usr/bin/env python
"""
Post-installation script for the astonai package.
Displays a message after installation about using the aston command.

This script is designed to run after installation is complete.
Users can also run it manually with:
    astonai-post-install
"""
import sys


def main():
    """Display information about the Aston AI package after installation."""
    show_message()
    return 0


def show_message():
    """Show the post-installation message."""
    green = "\033[92m" if sys.stdout.isatty() else ""
    bold = "\033[1m" if sys.stdout.isatty() else ""
    reset = "\033[0m" if sys.stdout.isatty() else ""
    
    message = f"""
{green}{bold}╭───────────────────────────────────────────╮{reset}
{green}{bold}│      Thank you for installing Aston AI     │{reset}
{green}{bold}╰───────────────────────────────────────────╯{reset}

{bold}IMPORTANT:{reset} Use the {green}aston{reset} command:

    {green}aston --help{reset}

"""
    print(message)


if __name__ == "__main__":
    sys.exit(main()) 
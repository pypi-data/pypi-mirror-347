#!/usr/bin/env python3
"""
GitHub PR Bot Runner

Starts the GitHub PR Comment Bot webhook service.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to sys.path if needed
script_dir = Path(__file__).resolve().parent
repo_root = script_dir.parent
sys.path.append(str(repo_root))

from testindex.api.coverage_map import app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("github-pr-bot")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the GitHub PR Comment Bot webhook service")
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=5000,
        help="Port to listen on (default: 5000)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Run in debug mode"
    )
    parser.add_argument(
        "--token",
        help="GitHub API token for posting comments (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--secret",
        help="GitHub webhook secret for signature validation (or set GITHUB_WEBHOOK_SECRET env var)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Set GitHub token and webhook secret if provided
    if args.token:
        os.environ["GITHUB_TOKEN"] = args.token
    
    if args.secret:
        os.environ["GITHUB_WEBHOOK_SECRET"] = args.secret
    
    # Check for required environment variables
    if not os.environ.get("GITHUB_TOKEN"):
        logger.warning("GITHUB_TOKEN environment variable not set! PR comments will not be posted.")
    
    if not os.environ.get("GITHUB_WEBHOOK_SECRET"):
        logger.warning("GITHUB_WEBHOOK_SECRET environment variable not set! Webhook validation disabled.")
    
    # Log startup message
    logger.info(f"Starting GitHub PR Bot webhook service on {args.host}:{args.port}")
    logger.info(f"Webhook URL: http://{args.host}:{args.port}/api/hooks/pr")
    
    # Run Flask app
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main() 
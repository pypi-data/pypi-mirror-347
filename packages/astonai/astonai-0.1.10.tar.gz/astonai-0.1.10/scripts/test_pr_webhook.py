#!/usr/bin/env python3
"""
GitHub Webhook Test Script

Simulates GitHub webhook calls for testing PR comment bot functionality.
"""

import os
import sys
import json
import argparse
import hmac
import hashlib
import requests
from pathlib import Path

# Sample PR webhook payload (simplified)
SAMPLE_PR_PAYLOAD = {
    "action": "opened",
    "number": 123,
    "pull_request": {
        "number": 123,
        "html_url": "https://github.com/owner/repo/pull/123",
        "title": "Test PR for webhook",
        "user": {
            "login": "test-user"
        },
        "head": {
            "ref": "feature-branch",
            "sha": "abc123"
        },
        "base": {
            "ref": "main",
            "sha": "def456"
        }
    },
    "repository": {
        "id": 12345,
        "name": "repo",
        "full_name": "owner/repo",
        "html_url": "https://github.com/owner/repo",
        "owner": {
            "login": "owner"
        }
    },
    "sender": {
        "login": "test-user"
    }
}

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test GitHub webhook functionality")
    parser.add_argument(
        "--url", 
        default="http://localhost:5000/api/hooks/pr",
        help="Webhook URL (default: http://localhost:5000/api/hooks/pr)"
    )
    parser.add_argument(
        "--secret",
        default=os.environ.get("GITHUB_WEBHOOK_SECRET", "test-secret"),
        help="GitHub webhook secret for signature validation (default: from GITHUB_WEBHOOK_SECRET env var or 'test-secret')"
    )
    parser.add_argument(
        "--action",
        choices=["opened", "synchronize", "reopened", "closed"],
        default="opened",
        help="PR action to simulate (default: opened)"
    )
    parser.add_argument(
        "--owner",
        default="test-owner",
        help="Repository owner (default: test-owner)"
    )
    parser.add_argument(
        "--repo",
        default="test-repo",
        help="Repository name (default: test-repo)"
    )
    parser.add_argument(
        "--pr",
        type=int,
        default=123,
        help="PR number (default: 123)"
    )
    
    return parser.parse_args()

def create_signature(payload, secret):
    """Create GitHub webhook signature."""
    mac = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha1
    )
    return 'sha1=' + mac.hexdigest()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Prepare payload with custom values
    payload = SAMPLE_PR_PAYLOAD.copy()
    payload["action"] = args.action
    payload["number"] = args.pr
    payload["pull_request"]["number"] = args.pr
    payload["repository"]["name"] = args.repo
    payload["repository"]["full_name"] = f"{args.owner}/{args.repo}"
    payload["repository"]["html_url"] = f"https://github.com/{args.owner}/{args.repo}"
    payload["repository"]["owner"]["login"] = args.owner
    
    # Convert payload to JSON
    payload_json = json.dumps(payload).encode('utf-8')
    
    # Create signature
    signature = create_signature(payload_json, args.secret)
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'pull_request',
        'X-Hub-Signature': signature,
        'X-GitHub-Delivery': 'test-delivery-id'
    }
    
    print(f"Sending webhook to {args.url}")
    print(f"Action: {args.action}")
    print(f"Repository: {args.owner}/{args.repo}")
    print(f"PR: #{args.pr}")
    
    # Send request
    try:
        response = requests.post(args.url, headers=headers, data=payload_json)
        
        print(f"\nResponse status: {response.status_code}")
        print("Response body:")
        try:
            # Try to parse JSON response
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            # If not JSON, print text
            print(response.text)
            
    except requests.RequestException as e:
        print(f"Error sending request: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
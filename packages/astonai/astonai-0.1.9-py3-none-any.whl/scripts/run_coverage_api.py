#!/usr/bin/env python3
"""
Run the Coverage Map API server.

This script starts the REST API server for the coverage map.
"""

import os
import sys
import socket
import argparse
import logging

# Add project root to path if running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testindex.api.coverage_map import run_api_server


def is_port_in_use(port):
    """Check if a port is in use.
    
    Args:
        port: Port number to check
        
    Returns:
        True if the port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port.
    
    Args:
        start_port: Port to start checking from
        max_attempts: Maximum number of ports to check
        
    Returns:
        Available port number, or None if no port is available
    """
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return None


def main():
    """Main entry point for API server."""
    parser = argparse.ArgumentParser(description="Run the Coverage Map API server")
    
    parser.add_argument("--host", default="0.0.0.0",
                       help="Host to bind to (default: 0.0.0.0)")
    
    parser.add_argument("--port", "-p", type=int, default=8080,
                       help="Port to listen on (default: 8080)")
    
    parser.add_argument("--debug", "-d", action="store_true",
                       help="Run in debug mode")
    
    parser.add_argument("--mock", "-m", action="store_true",
                       help="Use mock data instead of connecting to Neo4j")
    
    parser.add_argument("--auto-port", "-a", action="store_true",
                       help="Automatically find an available port if the specified port is in use")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger = logging.getLogger("coverage_api")
    
    # Check if the port is in use
    if is_port_in_use(args.port):
        if args.auto_port:
            # Find an available port
            new_port = find_available_port(args.port + 1)
            if new_port:
                logger.warning(f"Port {args.port} is in use, using port {new_port} instead")
                args.port = new_port
            else:
                logger.error(f"No available ports found in range {args.port + 1}-{args.port + 10}")
                logger.error("Please specify a different port with --port")
                sys.exit(1)
        else:
            logger.error(f"Port {args.port} is already in use")
            logger.error("Either specify a different port with --port or use --auto-port to automatically find an available port")
            logger.error("On macOS, AirPlay uses port 5000 by default. Try changing ports or disabling AirPlay Receiver.")
            sys.exit(1)
    
    # Log startup information
    logger.info(f"Starting Coverage Map API server at http://{args.host}:{args.port}")
    
    if args.mock:
        logger.info("Running in MOCK MODE - No Neo4j connection required")
        os.environ["USE_MOCK_DATA"] = "true"
    
    # Run server
    run_api_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main() 
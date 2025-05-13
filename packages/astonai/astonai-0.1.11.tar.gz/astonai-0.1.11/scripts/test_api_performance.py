#!/usr/bin/env python3
"""
Test API Performance

This script tests the performance of the Coverage Map API to ensure it meets
the dashboard load time KPI of <200ms.
"""

import os
import sys
import time
import argparse
import logging
import json
import statistics
from typing import List, Dict, Any
import requests

# Add project root to path if running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def setup_logging(verbose=False):
    """Setup logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("api_performance_test")


def test_api_endpoint(url: str, path: str, num_requests: int = 10) -> Dict[str, Any]:
    """Test API endpoint performance.
    
    Args:
        url: Base URL of the API
        path: Path to test with
        num_requests: Number of requests to make
        
    Returns:
        Dictionary with test metrics
    """
    request_times = []
    status_codes = []
    response_sizes = []
    
    full_url = f"{url}?path={path}"
    
    logger = logging.getLogger("api_performance_test")
    logger.info(f"Testing API endpoint: {full_url}")
    logger.info(f"Making {num_requests} requests...")
    
    for i in range(num_requests):
        logger.debug(f"Request {i+1}/{num_requests}")
        
        start_time = time.time()
        response = requests.get(full_url)
        end_time = time.time()
        
        request_time = (end_time - start_time) * 1000  # Convert to ms
        request_times.append(request_time)
        status_codes.append(response.status_code)
        
        if response.status_code == 200:
            response_sizes.append(len(response.content))
        
        # Add small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    # Calculate metrics
    avg_time = statistics.mean(request_times) if request_times else 0
    max_time = max(request_times) if request_times else 0
    min_time = min(request_times) if request_times else 0
    p95_time = sorted(request_times)[int(len(request_times) * 0.95)] if len(request_times) >= 20 else max_time
    success_rate = status_codes.count(200) / len(status_codes) if status_codes else 0
    avg_size = statistics.mean(response_sizes) if response_sizes else 0
    
    return {
        "path": path,
        "requests": num_requests,
        "avg_time_ms": avg_time,
        "min_time_ms": min_time,
        "max_time_ms": max_time,
        "p95_time_ms": p95_time,
        "success_rate": success_rate,
        "avg_response_size_bytes": avg_size,
        "meets_kpi": avg_time < 200  # KPI: <200ms load time
    }


def main():
    """Main entry point for performance test script."""
    parser = argparse.ArgumentParser(description="Test API performance")
    
    parser.add_argument("--url", default="http://localhost:8080/coverage-map",
                       help="API endpoint URL (default: http://localhost:8080/coverage-map)")
    
    parser.add_argument("--paths", nargs="+", required=True,
                       help="Paths to test (e.g. 'src' 'src/main.py')")
    
    parser.add_argument("--requests", "-n", type=int, default=10,
                       help="Number of requests per path (default: 10)")
    
    parser.add_argument("--output", "-o", type=str,
                       help="Path to output JSON file for results")
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    # Run tests for each path
    results = []
    for path in args.paths:
        result = test_api_endpoint(args.url, path, args.requests)
        results.append(result)
        
        logger.info(f"Results for path '{path}':")
        logger.info(f"  Average response time: {result['avg_time_ms']:.2f}ms")
        logger.info(f"  Max response time: {result['max_time_ms']:.2f}ms")
        logger.info(f"  Success rate: {result['success_rate'] * 100:.1f}%")
        logger.info(f"  Meets KPI (<200ms): {'YES' if result['meets_kpi'] else 'NO'}")
    
    # Calculate overall metrics
    avg_times = [r["avg_time_ms"] for r in results]
    overall_avg = statistics.mean(avg_times) if avg_times else 0
    all_meet_kpi = all(r["meets_kpi"] for r in results)
    
    logger.info(f"\nOverall Results:")
    logger.info(f"  Average response time across all paths: {overall_avg:.2f}ms")
    logger.info(f"  All paths meet KPI: {'YES' if all_meet_kpi else 'NO'}")
    
    # Write results to output file if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({
                "paths_tested": len(args.paths),
                "requests_per_path": args.requests,
                "overall_avg_time_ms": overall_avg,
                "all_meet_kpi": all_meet_kpi,
                "kpi_threshold_ms": 200,
                "results": results
            }, f, indent=2)
        logger.info(f"Results written to {args.output}")
    
    # Return success if all meet KPI, failure otherwise
    return 0 if all_meet_kpi else 1


if __name__ == "__main__":
    sys.exit(main()) 
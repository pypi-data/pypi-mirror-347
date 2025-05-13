#!/usr/bin/env python3
"""
Coverage Gap Detector CLI

Command-line tool for detecting code coverage gaps.
"""

import os
import sys
import argparse
import json
import logging
from datetime import datetime

# Add project root to path if running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testindex.analysis.coverage.gap_detector import GapDetector


def setup_logging(verbose=False):
    """Setup logging configuration."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("gap_detector")


def main():
    """Main entry point for the gap detector CLI."""
    parser = argparse.ArgumentParser(description="Detect code coverage gaps")
    
    parser.add_argument("--output", "-o", 
                        default=f"gaps_{datetime.now().strftime('%Y%m%d')}.json",
                        help="Output JSON file path")
    
    parser.add_argument("--threshold", "-t", type=float, default=0.0,
                        help="Coverage threshold (0-100)")
    
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose logging")
    
    parser.add_argument("--store", "-s", action="store_true",
                        help="Store gaps in Neo4j database")
    
    parser.add_argument("--batch-size", "-b", type=int, default=100,
                        help="Number of implementations to process in each batch")
    
    parser.add_argument("--previous-run", "-p", type=str,
                        help="Timestamp of previous run for change detection")
    
    parser.add_argument("--report-changes", "-c", type=str, 
                        help="Output file for changes report (JSON)")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    logger.info(f"Starting gap detection with threshold {args.threshold}%")
    
    try:
        # Initialize and run gap detector
        detector = GapDetector(
            coverage_threshold=args.threshold,
            batch_size=args.batch_size
        )
        
        # Record start time for performance monitoring
        start_time = datetime.now()
        
        # Find gaps
        gaps = detector.find_gaps()
        logger.info(f"Found {len(gaps)} gaps with coverage <= {args.threshold}%")
        
        # Export to JSON
        output_file = detector.export_gaps_json(args.output)
        logger.info(f"Exported gaps to {output_file}")
        
        # Store in Neo4j if requested
        if args.store:
            logger.info("Storing gaps in Neo4j...")
            stored_count = detector.store_gaps_in_neo4j()
            logger.info(f"Stored {stored_count} gaps in Neo4j")
        
        # Compare with previous run if specified
        if args.previous_run:
            logger.info(f"Detecting changes from previous run ({args.previous_run})...")
            changes = detector.find_changed_gaps(args.previous_run)
            
            logger.info(f"Changes detected: {len(changes['new_gaps'])} new, {len(changes['resolved_gaps'])} resolved")
            
            # Export changes report if requested
            if args.report_changes:
                # Get detailed information for new gaps
                new_gap_details = detector.get_gap_details(changes['new_gaps']) if changes['new_gaps'] else []
                
                # Get detailed information for resolved gaps
                resolved_gap_details = detector.get_gap_details(changes['resolved_gaps']) if changes['resolved_gaps'] else []
                
                # Generate report
                change_report = {
                    'timestamp': detector.run_timestamp,
                    'previous_run': args.previous_run,
                    'new_gaps_count': len(changes['new_gaps']),
                    'resolved_gaps_count': len(changes['resolved_gaps']),
                    'new_gaps': new_gap_details,
                    'resolved_gaps': resolved_gap_details
                }
                
                # Write report to file
                with open(args.report_changes, 'w') as f:
                    json.dump(change_report, f, indent=2)
                    
                logger.info(f"Wrote changes report to {args.report_changes}")
        
        # Report execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Gap detection completed in {execution_time:.2f} seconds")
        
        # Print summary
        print(f"\nGap Detection Summary:")
        print(f"----------------------")
        print(f"Total gaps found: {len(gaps)}")
        print(f"Coverage threshold: {args.threshold}%")
        print(f"Output file: {output_file}")
        if args.store:
            print(f"Gaps stored in Neo4j: {stored_count}")
        if args.previous_run:
            print(f"New gaps: {len(changes['new_gaps'])}")
            print(f"Resolved gaps: {len(changes['resolved_gaps'])}")
        
        # Return success
        return 0
        
    except Exception as e:
        logger.error(f"Error detecting gaps: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 
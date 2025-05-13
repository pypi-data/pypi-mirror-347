#!/usr/bin/env python3
"""
Validation Script for Coverage Gap Detection Precision

This script validates the precision of the gap detector by comparing
its output to ground truth coverage data from coverage.xml files.

Precision = True Positives / (True Positives + False Positives)
"""

import os
import sys
import argparse
import json
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Set, Tuple

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
    return logging.getLogger("precision_validator")


def parse_coverage_xml(xml_file: str) -> Dict[str, float]:
    """Parse a coverage.xml file and extract coverage data.
    
    Args:
        xml_file: Path to coverage.xml file
        
    Returns:
        Dictionary mapping file paths to coverage percentages
    """
    logger = logging.getLogger("precision_validator")
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        coverage_data = {}
        
        # Extract file-level coverage data
        for class_node in root.findall(".//class"):
            filename = class_node.attrib.get("filename", "")
            if not filename:
                continue
                
            # Get line coverage
            line_rate = float(class_node.attrib.get("line-rate", "0"))
            coverage_percentage = line_rate * 100
            
            coverage_data[filename] = coverage_percentage
            
        logger.info(f"Parsed {len(coverage_data)} files from {xml_file}")
        return coverage_data
        
    except Exception as e:
        logger.error(f"Error parsing {xml_file}: {str(e)}")
        return {}


def validate_against_coverage_xml(gaps_file: str, coverage_xml: str, threshold: float = 0.0) -> Tuple[float, Dict]:
    """Validate gap detection precision against coverage.xml.
    
    Args:
        gaps_file: Path to JSON file with detected gaps
        coverage_xml: Path to coverage.xml with ground truth
        threshold: Coverage threshold used for detection
        
    Returns:
        Tuple of (precision, metrics dictionary)
    """
    logger = logging.getLogger("precision_validator")
    
    # Load detected gaps
    with open(gaps_file, 'r') as f:
        gaps_data = json.load(f)
    
    detected_gaps = gaps_data.get('gaps', [])
    detected_files = {gap['path'] for gap in detected_gaps}
    
    # Parse coverage.xml
    coverage_data = parse_coverage_xml(coverage_xml)
    
    # Files with coverage below threshold in ground truth
    true_gaps = {file for file, coverage in coverage_data.items() if coverage <= threshold}
    
    # Calculate metrics
    true_positives = len(detected_files.intersection(true_gaps))
    false_positives = len(detected_files - true_gaps)
    false_negatives = len(true_gaps - detected_files)
    
    # Calculate precision and recall
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    # Calculate F1 score
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Compile metrics
    metrics = {
        'detected_gaps_count': len(detected_gaps),
        'ground_truth_gaps_count': len(true_gaps),
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }
    
    logger.info(f"Validation complete: Precision = {precision:.2f}, Recall = {recall:.2f}, F1 = {f1:.2f}")
    
    return precision, metrics


def main():
    """Main entry point for validation script."""
    parser = argparse.ArgumentParser(description="Validate gap detection precision")
    
    parser.add_argument("--gaps-file", "-g", required=True,
                        help="Path to JSON file with detected gaps")
    
    parser.add_argument("--coverage-xml", "-c", required=True,
                        help="Path to coverage.xml file with ground truth")
    
    parser.add_argument("--threshold", "-t", type=float, default=0.0,
                       help="Coverage threshold for validation (0-100)")
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    parser.add_argument("--output", "-o", type=str,
                       help="Path to output JSON file for metrics")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.verbose)
    
    # Validate precision
    precision, metrics = validate_against_coverage_xml(
        args.gaps_file, 
        args.coverage_xml,
        args.threshold
    )
    
    # Check against KPI
    precision_kpi = 0.95
    passed = precision >= precision_kpi
    logger.info(f"Precision KPI {'PASSED' if passed else 'FAILED'}: {precision:.2f} >= {precision_kpi}")
    
    # Write metrics to output file if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({
                'passed': passed,
                'precision_kpi': precision_kpi,
                'metrics': metrics
            }, f, indent=2)
        logger.info(f"Metrics written to {args.output}")
    
    # Print summary
    print(f"Validation Summary:")
    print(f"------------------")
    print(f"Detected gaps: {metrics['detected_gaps_count']}")
    print(f"Ground truth gaps: {metrics['ground_truth_gaps_count']}")
    print(f"True positives: {metrics['true_positives']}")
    print(f"False positives: {metrics['false_positives']}")
    print(f"False negatives: {metrics['false_negatives']}")
    print(f"Precision: {metrics['precision']:.2f}")
    print(f"Recall: {metrics['recall']:.2f}")
    print(f"F1 Score: {metrics['f1_score']:.2f}")
    print(f"KPI Status: {'PASSED' if passed else 'FAILED'}")
    
    # Return success if passed, failure if failed
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main()) 
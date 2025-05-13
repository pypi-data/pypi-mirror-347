#!/usr/bin/env python3
"""
Gap Detector CLI Demo

Demonstrates running the Gap Detector with mocked Neo4j responses.
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import our modules
from testindex.analysis.coverage.utils import SimpleNeo4jClient
from testindex.analysis.coverage.gap_detector import GapDetector

# Create a mock client
mock_client = MagicMock(spec=SimpleNeo4jClient)
mock_client.run_query.return_value = [
    {
        'id': 'F_example_func1',
        'path': 'src/module1.py',
        'line_start': 10,
        'line_end': 25,
        'coverage': 0.0
    },
    {
        'id': 'F_example_func2',
        'path': 'src/module2.py',
        'line_start': 15,
        'line_end': 30,
        'coverage': 0.0
    },
    {
        'id': 'C_ExampleClass',
        'path': 'src/module3.py',
        'line_start': 5,
        'line_end': 50,
        'coverage': 0.0
    }
]

# Initialize detector with mock client
detector = GapDetector(neo4j_client=mock_client)

# Demo output
print("===== Gap Detector Demo =====")

# Find gaps
gaps = detector.find_gaps()
print(f"\nFound {len(gaps)} coverage gaps:")

for i, gap in enumerate(gaps, 1):
    print(f"{i}. {gap['id']} ({gap['path']})")

# Export to JSON
output_file = 'demo_gaps.json'
detector.export_gaps_json(output_file)
print(f"\nGaps exported to {output_file}")

# Simulate Neo4j storage
with patch.object(mock_client, 'run_query', 
                 side_effect=[gaps] + [[{'gap_id': gap['id']}] for gap in gaps]):
    stored = detector.store_gaps_in_neo4j()
    print(f"\nStored {stored} gaps in Neo4j (simulated)")

print("\nDemo complete!") 
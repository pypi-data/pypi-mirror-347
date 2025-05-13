#!/usr/bin/env python3
"""
Create test schema data in Neo4j.

This script creates test nodes and relationships in Neo4j
based on the gold standard sample, so we can test the schema F1 scoring.
"""

import os
import sys
import json
import argparse
from pathlib import Path

from testindex.knowledge.graph.neo4j_client import Neo4jClient, Neo4jConfig

def load_gold_standard(file_path: str):
    """Load the gold standard from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Basic validation
        if not isinstance(data, dict) or 'nodes' not in data or 'edges' not in data:
            raise ValueError("Invalid gold standard format. Expected 'nodes' and 'edges' keys.")
        
        return data
    except Exception as e:
        print(f"Error loading gold standard: {e}")
        sys.exit(1)

def create_test_data(client: Neo4jClient, gold_data, add_extras=False):
    """Create test nodes and relationships in Neo4j based on gold standard data."""
    # Clear existing data
    print("Clearing existing data...")
    client.execute_query("MATCH (n) DETACH DELETE n")
    
    # Create nodes
    print("Creating nodes...")
    for node in gold_data['nodes']:
        labels = ':'.join(node['labels'])
        query = f"""
        CREATE (n:{labels} {{id: $id}})
        """
        client.execute_query(query, {"id": node['id']})
    
    # Create relationships
    print("Creating relationships...")
    for edge in gold_data['edges']:
        query = f"""
        MATCH (source {{id: $src}})
        MATCH (target {{id: $dst}})
        CREATE (source)-[:{edge['type']}]->(target)
        """
        client.execute_query(query, {"src": edge['src'], "dst": edge['dst']})
    
    # Add some extras for precision testing if requested
    if add_extras:
        print("Adding extra nodes and relationships for precision testing...")
        # Add an extra node
        extra_node_id = "F_extra_function_99"
        client.execute_query(
            "CREATE (n:Implementation {id: $id})",
            {"id": extra_node_id}
        )
        
        # Add an extra relationship
        if len(gold_data['nodes']) >= 2:
            # Use the first node as source and second as target
            src = gold_data['nodes'][0]['id']
            dst = gold_data['nodes'][1]['id']
            client.execute_query(
                "MATCH (source {id: $src}) MATCH (target {id: $dst}) CREATE (source)-[:EXTRA_REL]->(target)",
                {"src": src, "dst": dst}
            )
    
    # Count created data
    node_count = client.execute_query("MATCH (n) RETURN count(n) as count")[0]['count']
    rel_count = client.execute_query("MATCH ()-[r]->() RETURN count(r) as count")[0]['count']
    
    print(f"Created {node_count} nodes and {rel_count} relationships in Neo4j.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create test schema data in Neo4j.")
    parser.add_argument("--gold-file", default="benchmarks/gold_schema.json", 
                        help="Path to gold standard file to use as reference")
    parser.add_argument("--add-extras", action="store_true",
                        help="Add extra nodes and relationships to test precision")
    
    args = parser.parse_args()
    
    # Check if Neo4j environment variables are set
    neo4j_uri = os.environ.get("NEO4J_URI")
    neo4j_user = os.environ.get("NEO4J_USER")
    neo4j_pass = os.environ.get("NEO4J_PASS")
    
    if not all([neo4j_uri, neo4j_user, neo4j_pass]):
        print("Error: Neo4j environment variables not set.")
        print("Please set NEO4J_URI, NEO4J_USER, and NEO4J_PASS")
        sys.exit(1)
    
    # Load the gold standard
    print(f"Loading gold standard from {args.gold_file}...")
    gold_data = load_gold_standard(args.gold_file)
    print(f"Loaded {len(gold_data['nodes'])} nodes and {len(gold_data['edges'])} edges from gold standard.")
    
    # Connect to Neo4j
    print(f"Connecting to Neo4j at {neo4j_uri}...")
    neo4j_config = Neo4jConfig(
        uri=neo4j_uri,
        username=neo4j_user,
        password=neo4j_pass
    )
    
    neo4j_client = Neo4jClient(neo4j_config)
    
    # Create test data
    create_test_data(neo4j_client, gold_data, args.add_extras)
    
    print("Test data creation complete.")

if __name__ == "__main__":
    main() 
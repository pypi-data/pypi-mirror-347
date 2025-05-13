"""
TestIndex coverage command.

This module implements the `testindex coverage` command that displays test coverage gaps.
"""
import os
import sys
import json as json_lib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import datetime
import shutil

import click
from rich.console import Console
from rich.table import Table

from testindex.core.cli.runner import common_options
from testindex.core.config import ConfigModel, ConfigLoader
from testindex.core.exceptions import CLIError
from testindex.core.logging import get_logger
from testindex.analysis.coverage.ingest import ingest_coverage, find_coverage_file, has_coverage_data
from testindex.core.path_resolution import PathResolver

# Set up logger
logger = get_logger(__name__)

# Constants
DEFAULT_CONFIG_DIR = ".testindex"
DEFAULT_CONFIG_FILE = "config.yml"
DEFAULT_THRESHOLD = 0  # Default: report only zero coverage (true gaps)


def load_config() -> Dict[str, Any]:
    """Load configuration from file or environment variables.
    
    Fallback order: 
    1. .testindex/config.yml 
    2. environment variables 
    3. defaults
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    
    Raises:
        CLIError: If configuration cannot be loaded
    """
    try:
        # 1. Try to load from .testindex/config.yml
        config_path = Path(DEFAULT_CONFIG_DIR) / DEFAULT_CONFIG_FILE
        if config_path.exists():
            logger.info(f"Loading config from {config_path}")
            import yaml
            
            # Read raw content for debugging
            with open(config_path, 'r') as f:
                raw_content = f.read()
                logger.info(f"Raw config content: {raw_content}")
            
            # Parse YAML
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                
                # Add default values if missing
                if 'offline_mode' not in config_data:
                    config_data['offline_mode'] = True
                if 'knowledge_graph_dir' not in config_data:
                    config_data['knowledge_graph_dir'] = str(Path(DEFAULT_CONFIG_DIR) / "knowledge_graph")

                logger.info(f"Parsed config data: {config_data}")
                return config_data
        
        # 2. Try to load from environment variables
        neo4j_uri = os.environ.get("NEO4J_URI")
        if neo4j_uri:
            logger.info("Loading config from environment variables")
            return {
                "neo4j_uri": neo4j_uri,
                "neo4j_user": os.environ.get("NEO4J_USER", "neo4j"),
                "neo4j_password": os.environ.get("NEO4J_PASSWORD", ""),
                "vector_store": os.environ.get("VECTOR_STORE_PATH", "vectors.sqlite"),
                "schema_version": "K1"
            }
        
        # 3. Use defaults (offline mode)
        logger.info("Using default offline configuration")
        return {
            "neo4j_uri": None,
            "vector_store": None,
            "schema_version": "K1",
            "offline_mode": True,
            "knowledge_graph_dir": Path(DEFAULT_CONFIG_DIR) / "knowledge_graph"
        }
    
    except Exception as e:
        error_msg = f"Failed to load configuration: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_coverage_gaps(config: Dict[str, Any], threshold: int = DEFAULT_THRESHOLD) -> Tuple[List[Dict[str, Any]], int]:
    """Detect implementations with test coverage below threshold.
    
    Args:
        config: Configuration dictionary
        threshold: Coverage percentage threshold (0-100)
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If gap detection fails
    """
    try:
        # Check if we're in offline mode
        offline_mode = config.get("offline_mode", False)
        logger.info(f"Config values: {config}")
        logger.info(f"Offline mode detected: {offline_mode}")
        
        if offline_mode:
            logger.info("Running gap detection in offline mode")
            return detect_gaps_from_local_json(config, threshold)
        else:
            logger.info("Running gap detection with Neo4j")
            return detect_gaps_from_neo4j(config, threshold)
            
    except Exception as e:
        error_msg = f"Failed to detect coverage gaps: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_gaps_from_neo4j(config: Dict[str, Any], threshold: int) -> Tuple[List[Dict[str, Any]], int]:
    """Detect coverage gaps using Neo4j.
    
    Args:
        config: Configuration dictionary with Neo4j connection details
        threshold: Coverage percentage threshold
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If Neo4j query fails
    """
    try:
        # Import Neo4j client
        from testindex.knowledge.graph.neo4j_client import Neo4jClient, Neo4jConfig
        
        # Create Neo4j config
        neo4j_config = Neo4jConfig(
            uri=config.get("neo4j_uri"),
            username=config.get("neo4j_user", "neo4j"),
            password=config.get("neo4j_password", "")
        )
        
        # Connect to Neo4j
        client = Neo4jClient(neo4j_config)
        
        # Define query for implementations below threshold
        query = """
        MATCH (i:Implementation)
        WHERE i.coverage IS NULL OR i.coverage <= $threshold
        RETURN i.file_path as file, i.name as function, 
               COALESCE(i.coverage, 0) as coverage
        ORDER BY i.file_path, i.name
        """
        
        # Execute query
        result = client.run_query(query, {"threshold": threshold})
        
        # Process results
        gaps = []
        for record in result:
            gaps.append({
                "file": record["file"],
                "function": record["function"],
                "coverage": record["coverage"]
            })
        
        # Get total implementations count
        count_query = "MATCH (i:Implementation) RETURN count(i) as count"
        count_result = client.run_query(count_query)
        total_impls = count_result[0]["count"] if count_result else 0
        
        logger.info(f"Found {len(gaps)} gaps out of {total_impls} implementations")
        return gaps, total_impls
        
    except ImportError:
        logger.error("Neo4j client not available. Install with pip install neo4j")
        raise CLIError("Neo4j client not available")
    except Exception as e:
        error_msg = f"Neo4j gap detection failed: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def detect_gaps_from_local_json(config: Dict[str, Any], threshold: int) -> Tuple[List[Dict[str, Any]], int]:
    """Detect coverage gaps using local JSON files.
    
    Args:
        config: Configuration dictionary with paths
        threshold: Coverage percentage threshold
        
    Returns:
        Tuple[List[Dict[str, Any]], int]: List of gaps and total implementation count
        
    Raises:
        CLIError: If JSON files cannot be read
    """
    try:
        import json
        
        # Get path to knowledge graph directory
        kg_dir = config.get("knowledge_graph_dir", Path(DEFAULT_CONFIG_DIR) / "knowledge_graph")
        
        if isinstance(kg_dir, str):
            kg_dir = Path(kg_dir)
            
        logger.info(f"Looking for nodes.json in: {kg_dir}")
            
        # Check if nodes.json exists
        nodes_file = kg_dir / "nodes.json"
        if not nodes_file.exists():
            raise CLIError(f"Nodes file not found: {nodes_file}")
            
        # Load nodes
        with open(nodes_file, 'r') as f:
            nodes = json.load(f)
            
        # Filter for implementations
        implementations = []
        for node in nodes:
            # Check if it's an implementation node (not a module)
            if node.get("type") == "Implementation":
                # Extract properties
                props = node.get("properties", {})
                
                # Default coverage to 0 if not present
                coverage = props.get("coverage", 0)
                
                implementations.append({
                    "id": node.get("id", "unknown"),
                    "file": node.get("file_path", "unknown"),
                    "function": node.get("name", "unknown"),
                    "coverage": coverage
                })
        
        # Log some sample implementations for debugging
        logger.debug("Sample implementations:")
        for impl in implementations[:5]:
            logger.debug(f"  File: {impl['file']}, Function: {impl['function']}, Coverage: {impl['coverage']}")
        
        # Filter for gaps
        gaps = [impl for impl in implementations if impl["coverage"] <= threshold]
        
        # Log all implementations with coverage > 0 for debugging
        covered_impls = [impl for impl in implementations if impl["coverage"] > 0]
        logger.debug(f"Found {len(covered_impls)} implementations with coverage > 0:")
        for impl in covered_impls[:20]:  # Show up to 20
            logger.debug(f"  Covered: {impl['file']} - {impl['function']} ({impl['coverage']}%)")
        
        # Calculate percentage for summary
        gap_percentage = (len(gaps) / len(implementations)) * 100 if implementations else 0
        logger.info(f"Found {len(gaps)} gaps out of {len(implementations)} implementations ({gap_percentage:.1f}%)")
        
        return gaps, len(implementations)
        
    except Exception as e:
        error_msg = f"Local JSON gap detection failed: {e}"
        logger.error(error_msg)
        raise CLIError(error_msg)


def output_table(gaps: List[Dict[str, Any]], total_impls: int = None) -> None:
    """Output coverage gaps as a rich table to stdout.
    
    Args:
        gaps: List of coverage gaps
        total_impls: Total implementation count
    """
    console = Console()
    
    # Create table
    table = Table(title="Coverage Gaps")
    
    # Add columns
    table.add_column("File", style="cyan")
    table.add_column("Function", style="green")
    table.add_column("%Cov", justify="right", style="yellow")
    
    # Add rows
    for gap in gaps:
        file_path = gap.get("file", "")
        function = gap.get("function", "")
        coverage = gap.get("coverage", 0)
        
        # Add row
        table.add_row(
            str(file_path),
            str(function),
            str(coverage)
        )
    
    # Print table
    console.print(table)
    
    # Print summary
    if total_impls is not None:
        gap_percent = len(gaps) / total_impls * 100 if total_impls > 0 else 0
        console.print(f"Gaps: {len(gaps)} / {total_impls} implementations ({gap_percent:.1f}%)")


def output_json(gaps: List[Dict[str, Any]], output_path: str, repo_info: Dict[str, Any] = None, total_impls: int = None) -> None:
    """Output coverage gaps as JSON to the specified path.
    
    Args:
        gaps: List of coverage gaps
        output_path: Path to output JSON file
        repo_info: Repository information
        total_impls: Total implementation count
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Create output data
    timestamp = datetime.datetime.now().isoformat()
    
    output_data = {
        "version": "v1",  # Add version for backward compatibility
        "metadata": {
            "timestamp": timestamp,
            "total_implementations": total_impls,
            "gap_count": len(gaps),
            "coverage_percentage": (1 - len(gaps) / total_impls) * 100 if total_impls and total_impls > 0 else 0
        },
        "repository": repo_info or {},
        "gaps": gaps,
        "schema_version": "1.0"
    }
    
    # Write to file
    with open(output_path, 'w') as f:
        json_lib.dump(output_data, f, indent=2)
    
    logger.info(f"Wrote {len(gaps)} gaps to {output_path}")


def get_repo_info() -> Dict[str, Any]:
    """Get information about the current repository.
    
    Returns:
        Dict[str, Any]: Repository information including SHA
    """
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        sha = result.stdout.strip()
        return {"sha": sha}
    except Exception:
        return {"sha": "unknown"}


def ensure_coverage_file(coverage_file: Optional[str]) -> Optional[str]:
    """Ensure that a coverage file is available.
    
    If coverage file is specified, verify it exists.
    If not specified, try to find it in common locations.
    
    Args:
        coverage_file: Path to coverage file, or None to search
        
    Returns:
        Path to coverage file if found
        
    Raises:
        CLIError: If coverage file is not found
    """
    if coverage_file:
        # User specified a coverage file, ensure it exists
        if not Path(coverage_file).exists():
            raise CLIError(f"Coverage file not found: {coverage_file}")
        logger.info(f"Using specified coverage file: {coverage_file}")
        return coverage_file
    
    # Try to find coverage file using PathResolver
    coverage_path = PathResolver.find_coverage_file()
    if coverage_path:
        logger.info(f"Found coverage file at: {coverage_path}")
        return str(coverage_path)
    
    # No coverage file found
    raise CLIError(
        "No coverage file found. Run your tests with coverage first:\n"
        "  pytest --cov --cov-report=xml\n"
        "Or use our helper command:\n"
        "  aston test"
    )


@click.command('coverage', help='Display test coverage gaps')
@click.option('--json', 'json_output', type=click.Path(), help='Output gaps in JSON format')
@click.option('--exit-on-gap', is_flag=True, help='Return exit code 1 if gaps exist')
@click.option('--threshold', type=int, default=DEFAULT_THRESHOLD, 
              help=f'Coverage percentage threshold (0-100, default: {DEFAULT_THRESHOLD})')
@click.option('--coverage-file', type=click.Path(exists=True), 
              help='Path to coverage.xml file to ingest before checking gaps')
@common_options
def coverage_command(json_output, exit_on_gap, threshold, coverage_file, verbose, summary_only, **kwargs):
    """Display test coverage gaps.
    
    This command:
    1. Ingests coverage data from coverage.xml
    2. Identifies implementation nodes with test coverage below threshold
    3. Displays a table of coverage gaps
    
    Exit codes:
    - 0: Success (no gaps found or gaps found but not using --exit-on-gap)
    - 1: Gaps found (when using --exit-on-gap)
    - 2: Error occurred
    """
    try:
        # Create console for rich output
        console = Console()
        
        # First, make sure we have a coverage file
        if not coverage_file:
            try:
                coverage_file = ensure_coverage_file(None)
            except CLIError as e:
                console.print(f"[bold red]Error:[/] {str(e)}")
                console.print("[bold yellow]Hint:[/] Run tests with coverage using:")
                console.print("  [green]pytest --cov --cov-report=xml[/]")
                console.print("  or")
                console.print("  [green]aston test[/]")
                return 2
        
        # Check if coverage file has coverage data
        if not has_coverage_data(coverage_file):
            console.print("[bold yellow]Warning:[/] Coverage file exists but contains no coverage data")
            console.print("[bold yellow]Hint:[/] Run tests with coverage using:")
            console.print("  [green]pytest --cov --cov-report=xml[/]")
            console.print("  or")
            console.print("  [green]aston test[/]")
            return 2
        
        # Load config
        if not summary_only:
            console.print("🧠 Loading knowledge graph...")
        config = load_config()
        
        # Ingest coverage data if we have a file
        if coverage_file:
            if not summary_only:
                console.print(f"📄 Reading coverage.xml...")
            ingest_coverage(config, coverage_file)
        
        # Detect gaps
        if not summary_only:
            console.print("🔍 Detecting coverage gaps...")
        gaps, total_impls = detect_coverage_gaps(config, threshold)
        
        # Generate repo info
        repo_info = get_repo_info()
        
        # Show summary
        if not summary_only:
            console.print("📊 Summary:")
            
            # Collect statistics
            covered_impls = total_impls - len(gaps)
            covered_percent = (covered_impls / total_impls * 100) if total_impls > 0 else 0
            gap_percent = (len(gaps) / total_impls * 100) if total_impls > 0 else 0
            
            # Create a table for the summary
            table = Table(show_header=False, box=None)
            table.add_column("Name", style="dim")
            table.add_column("Value", style="bold")
            
            table.add_row("Total nodes", f"{total_impls}")
            table.add_row("Covered", f"{covered_impls} ({covered_percent:.1f}%)")
            table.add_row("Uncovered", f"{len(gaps)} ({gap_percent:.1f}%)")
            
            console.print(table)
        
        # Collect files with most gaps
        if gaps:
            file_gaps = {}
            for gap in gaps:
                file_path = gap["file"]
                if file_path not in file_gaps:
                    file_gaps[file_path] = 0
                file_gaps[file_path] += 1
            
            # Sort files by number of gaps
            sorted_files = sorted(file_gaps.items(), key=lambda x: x[1], reverse=True)
            
            # Show top uncovered files
            if not summary_only:
                console.print("\n📌 Top uncovered:")
                for file_path, count in sorted_files[:5]:  # Show top 5
                    console.print(f"- {file_path} ({count})")
            
            # Output table of gaps
            if not summary_only and not json_output:
                output_table(gaps, total_impls)
            
            # Export gaps to JSON if requested
            if json_output:
                output_json(gaps, json_output, repo_info, total_impls)
                if not summary_only:
                    console.print(f"💾 Gaps exported to {json_output}")
            
            # Also save gaps to .aston/gaps.json for easy access
            aston_dir = Path(".aston")
            if not aston_dir.exists():
                aston_dir.mkdir(exist_ok=True)
            output_json(gaps, str(aston_dir / "gaps.json"), repo_info, total_impls)
            
            # Check for exit-on-gap
            if exit_on_gap:
                if not summary_only:
                    console.print("[yellow]Gaps found and --exit-on-gap specified, exiting with code 1[/]")
                return 1
        else:
            # No gaps found
            if not summary_only:
                console.print("\n🎉 No coverage gaps found!")
            
            # Output empty JSON if requested
            if json_output:
                output_json([], json_output, repo_info, total_impls)
                if not summary_only:
                    console.print(f"💾 Empty gaps file exported to {json_output}")
        
        # Success
        return 0
        
    except CLIError as e:
        console = Console()
        console.print(f"[bold red]Error:[/] {str(e)}")
        return 2
    except Exception as e:
        console = Console()
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        return 2 
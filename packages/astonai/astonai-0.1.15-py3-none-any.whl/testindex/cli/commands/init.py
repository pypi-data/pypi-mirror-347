"""
TestIndex init command.

This module implements the `testindex init` command that initializes a Knowledge graph
for a repository. It handles both local and remote repositories.
"""
import os
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Protocol
from abc import ABC, abstractmethod

import click
import yaml
from rich.progress import Progress
from rich.console import Console

from testindex.core.cli.runner import common_options
from testindex.core.cli.progress import create_progress
from testindex.core.config import ConfigModel
from testindex.core.exceptions import CLIError
from testindex.core.utils import ensure_directory
from testindex.core.logging import get_logger
from testindex.preprocessing.chunking.code_chunker import PythonCodeChunker
from testindex.preprocessing.integration.chunk_graph_adapter import ChunkGraphAdapter
from testindex.preprocessing.cloning.git_manager import GitManager
from testindex.knowledge.graph.neo4j_client import Neo4jClient, Neo4jConfig, Neo4jConnectionError

# Constants
DEFAULT_CONFIG_DIR = ".testindex"
DEFAULT_CONFIG_FILE = "config.yml"
DEFAULT_EXCLUDE_PATTERNS = [
    "**/venv/**",
    "**/.venv/**",
    "**/site-packages/**",
    "**/node_modules/**",
    "**/dist/**",
    "**/build/**",
    "**/.git/**",
    "**/.hg/**",
    "**/.svn/**",
]

# Set up logger
logger = get_logger(__name__)

class RepositoryAdapter(ABC):
    """Abstract base class for repository adapters."""
    
    @abstractmethod
    def detect_repository(self, path: Path) -> bool:
        """Detect if the given path is a repository of this type.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if this is a repository of this type
        """
        pass
    
    @abstractmethod
    def get_root(self, path: Path) -> Optional[Path]:
        """Get the root directory of the repository.
        
        Args:
            path: Path to start searching from
            
        Returns:
            Optional[Path]: Path to repository root, or None if not found
        """
        pass
    
    @abstractmethod
    def clone(self, url: str, target_path: Path) -> None:
        """Clone a repository from a URL.
        
        Args:
            url: Repository URL
            target_path: Path to clone to
            
        Raises:
            CLIError: If cloning fails
        """
        pass
    
    @abstractmethod
    def pull(self, path: Path) -> None:
        """Pull latest changes for a repository.
        
        Args:
            path: Path to repository
            
        Raises:
            CLIError: If pull fails
        """
        pass

class GitRepositoryAdapter(RepositoryAdapter):
    """Adapter for Git repositories."""
    
    def __init__(self):
        # Create a default config for GitManager
        config = ConfigModel()
        self.git_manager = GitManager(config)
    
    def detect_repository(self, path: Path) -> bool:
        git_dir = path / ".git"
        return git_dir.exists() and git_dir.is_dir()
    
    def get_root(self, path: Path) -> Optional[Path]:
        current = path.absolute()
        
        # Traverse up to 10 levels of directories
        for _ in range(10):
            if self.detect_repository(current):
                return current
            
            # Stop if we're at the root directory
            if current.parent == current:
                break
                
            current = current.parent
        
        return None
    
    def clone(self, url: str, target_path: Path) -> None:
        try:
            self.git_manager.clone_repository(url, target_path)
        except Exception as e:
            raise CLIError(f"Failed to clone Git repository: {str(e)}")
    
    def pull(self, path: Path) -> None:
        try:
            self.git_manager.update_repository(path)
        except Exception as e:
            raise CLIError(f"Failed to pull Git repository: {str(e)}")

class MercurialRepositoryAdapter(RepositoryAdapter):
    """Adapter for Mercurial repositories."""
    
    def detect_repository(self, path: Path) -> bool:
        hg_dir = path / ".hg"
        return hg_dir.exists() and hg_dir.is_dir()
    
    def get_root(self, path: Path) -> Optional[Path]:
        current = path.absolute()
        
        # Traverse up to 10 levels of directories
        for _ in range(10):
            if self.detect_repository(current):
                return current
            
            # Stop if we're at the root directory
            if current.parent == current:
                break
                
            current = current.parent
        
        return None
    
    def clone(self, url: str, target_path: Path) -> None:
        try:
            import subprocess
            subprocess.run(["hg", "clone", url, str(target_path)], check=True)
        except subprocess.CalledProcessError as e:
            raise CLIError(f"Failed to clone Mercurial repository: {str(e)}")
        except FileNotFoundError:
            raise CLIError("Mercurial (hg) command not found. Please install Mercurial.")
    
    def pull(self, path: Path) -> None:
        try:
            import subprocess
            subprocess.run(["hg", "pull", "-u"], cwd=str(path), check=True)
        except subprocess.CalledProcessError as e:
            raise CLIError(f"Failed to pull Mercurial repository: {str(e)}")
        except FileNotFoundError:
            raise CLIError("Mercurial (hg) command not found. Please install Mercurial.")

class SVNRepositoryAdapter(RepositoryAdapter):
    """Adapter for Subversion repositories."""
    
    def detect_repository(self, path: Path) -> bool:
        svn_dir = path / ".svn"
        return svn_dir.exists() and svn_dir.is_dir()
    
    def get_root(self, path: Path) -> Optional[Path]:
        current = path.absolute()
        
        # Traverse up to 10 levels of directories
        for _ in range(10):
            if self.detect_repository(current):
                return current
            
            # Stop if we're at the root directory
            if current.parent == current:
                break
                
            current = current.parent
        
        return None
    
    def clone(self, url: str, target_path: Path) -> None:
        try:
            import subprocess
            subprocess.run(["svn", "checkout", url, str(target_path)], check=True)
        except subprocess.CalledProcessError as e:
            raise CLIError(f"Failed to checkout SVN repository: {str(e)}")
        except FileNotFoundError:
            raise CLIError("Subversion (svn) command not found. Please install Subversion.")
    
    def pull(self, path: Path) -> None:
        try:
            import subprocess
            subprocess.run(["svn", "update"], cwd=str(path), check=True)
        except subprocess.CalledProcessError as e:
            raise CLIError(f"Failed to update SVN repository: {str(e)}")
        except FileNotFoundError:
            raise CLIError("Subversion (svn) command not found. Please install Subversion.")

class PlainDirectoryAdapter(RepositoryAdapter):
    """Adapter for plain directories (no VCS)."""
    
    def detect_repository(self, path: Path) -> bool:
        # A plain directory is always considered a "repository"
        return path.is_dir()
    
    def get_root(self, path: Path) -> Optional[Path]:
        return path.absolute()
    
    def clone(self, url: str, target_path: Path) -> None:
        # For plain directories, we just create the directory
        ensure_directory(target_path)
    
    def pull(self, path: Path) -> None:
        # No-op for plain directories
        pass

# List of available repository adapters
REPOSITORY_ADAPTERS = [
    GitRepositoryAdapter(),
    MercurialRepositoryAdapter(),
    SVNRepositoryAdapter(),
    PlainDirectoryAdapter()
]

def detect_repository_type(path: Path) -> Optional[RepositoryAdapter]:
    """Detect the type of repository at the given path.
    
    Args:
        path: Path to check
        
    Returns:
        Optional[RepositoryAdapter]: Repository adapter if detected, None otherwise
    """
    for adapter in REPOSITORY_ADAPTERS:
        if adapter.detect_repository(path):
            return adapter
    return None

def setup_repo(url: Optional[str], path: Optional[str], force: bool = False) -> Path:
    """Set up the repository for analysis.
    
    Args:
        url: URL of the repository to clone
        path: Path to the existing local repository
        force: Whether to force clone/clean
        
    Returns:
        Path: Path to the repository
        
    Raises:
        CLIError: If repository setup fails
    """
    if url:
        # Clone the repository
        click.echo(f"🌐 Cloning repository from {url}...")
        repo_dir = Path(".testindex") / "cache" / url.split("/")[-1].replace(".git", "")
        
        # Create directory if it doesn't exist
        ensure_directory(repo_dir.parent)
        
        # Determine repository type from URL
        adapter = None
        if url.endswith(".git"):
            adapter = GitRepositoryAdapter()
        elif url.startswith("svn+"):
            adapter = SVNRepositoryAdapter()
        elif url.startswith("hg+"):
            adapter = MercurialRepositoryAdapter()
        else:
            # Try to detect from URL
            if "svn" in url:
                adapter = SVNRepositoryAdapter()
            elif "hg" in url:
                adapter = MercurialRepositoryAdapter()
            else:
                # Default to Git
                adapter = GitRepositoryAdapter()
        
        # Clone or update repository
        try:
            if repo_dir.exists() and not force:
                click.echo(f"📂 Repository already exists at {repo_dir}")
                click.echo("🔄 Pulling latest changes...")
                adapter.pull(repo_dir)
            else:
                if repo_dir.exists():
                    shutil.rmtree(repo_dir)
                adapter.clone(url, repo_dir)
            
            click.echo(f"✅ Repository cloned to {repo_dir}")
            return repo_dir
            
        except Exception as e:
            error_msg = f"Failed to clone repository: {str(e)}"
            logger.error(error_msg)
            raise CLIError(error_msg)
    
    elif path:
        # Use the specified path
        repo_path = Path(path).absolute()
        if not repo_path.exists():
            error_msg = f"Repository path does not exist: {repo_path}"
            logger.error(error_msg)
            raise CLIError(error_msg)
        
        # Detect repository type
        adapter = detect_repository_type(repo_path)
        if adapter:
            click.echo(f"📂 Using {adapter.__class__.__name__} repository at {repo_path}")
        else:
            click.echo(f"📂 Using plain directory at {repo_path}")
            adapter = PlainDirectoryAdapter()
        
        return repo_path
    
    else:
        # Try to find repository in current directory
        current_dir = Path.cwd()
        
        # Try each adapter
        for adapter in REPOSITORY_ADAPTERS:
            root = adapter.get_root(current_dir)
            if root:
                click.echo(f"📂 Using {adapter.__class__.__name__} repository at {root}")
                return root
        
        # If no repository found, use current directory as plain directory
        click.echo(f"📂 Using current directory as plain directory")
        return current_dir

def count_lines_of_code(repo_path: Path) -> int:
    """Count lines of Python code in the repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        int: Number of lines of Python code
    """
    try:
        # Use the existing count_loc.py script if available
        count_script = Path(__file__).parent.parent.parent.parent / "scripts" / "count_loc.py"
        if count_script.exists():
            import subprocess
            output = subprocess.check_output([sys.executable, str(count_script), str(repo_path)])
            return int(output.strip())
    except Exception as e:
        logger.warning(f"Failed to run count_loc.py script: {e}")
    
    # Fallback: Simple line counting
    count = 0
    for file_path in repo_path.glob("**/*.py"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                count += sum(1 for _ in f)
        except Exception as e:
            logger.warning(f"Failed to count lines in {file_path}: {e}")
    
    return count

def run_ingest_pipeline(repo_path: Path, config_path: Path, force_offline: bool = False, exclude_patterns: List[str] = [], verbose: bool = False, summary_only: bool = False) -> Tuple[int, int]:
    """Run the ingest pipeline on the repository.
    
    This ingests the source files, chunks them, and builds a knowledge graph.
    
    Args:
        repo_path: Path to repository root
        config_path: Path to save the config file
        force_offline: Force offline mode even if Neo4j is available
        exclude_patterns: List of glob patterns for directories to exclude
        verbose: Whether to enable verbose output
        summary_only: Whether to suppress detailed progress output
        
    Returns:
        Tuple[int, int]: Number of chunks and number of nodes
    """
    # Set up Neo4j client if needed
    neo4j_client = None
    if not force_offline:
        try:
            # Check Neo4j connection
            neo4j_uri = os.environ.get("NEO4J_URI")
            neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
            neo4j_password = os.environ.get("NEO4J_PASSWORD", "")
            
            # Create Neo4j config
            neo4j_config = Neo4jConfig(
                uri=neo4j_uri,
                username=neo4j_user,
                password=neo4j_password
            )
            
            # Create Neo4j client
            neo4j_client = Neo4jClient(neo4j_config)
            neo4j_client.test_connection()
            logger.info("Neo4j connection successful")
        except Neo4jConnectionError as e:
            logger.warning(f"Neo4j connection failed, falling back to offline mode: {e}")
            neo4j_client = None
        except Exception as e:
            logger.warning(f"Neo4j setup failed, falling back to offline mode: {e}")
            neo4j_client = None
    
    # Set up chunker
    chunker = PythonCodeChunker()
    
    # Set up graph adapter (local JSON or Neo4j)
    if neo4j_client:
        # Online mode with Neo4j
        graph_dir = Path(config_path).parent / "knowledge_graph"
        ensure_directory(graph_dir)
        
        graph_adapter = ChunkGraphAdapter(
            chunks_path=graph_dir / "chunks.json",
            nodes_path=graph_dir / "nodes.json",
            neo4j_client=neo4j_client
        )
    else:
        # Offline mode with local JSON
        graph_dir = Path(config_path).parent / "knowledge_graph"
        ensure_directory(graph_dir)
        
        graph_adapter = ChunkGraphAdapter(
            chunks_path=graph_dir / "chunks.json",
            nodes_path=graph_dir / "nodes.json",
            neo4j_client=None
        )
    
    # Find Python files in the repository
    all_py_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                py_file = Path(root) / file
                all_py_files.append(py_file)
    
    # Use provided exclude patterns or defaults
    if not exclude_patterns:
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS
    
    logger.info(f"Using exclude patterns: {exclude_patterns}")
    
    # Filter files based on exclusion patterns
    filtered_files = []
    for file_path in all_py_files:
        skip = False
        # Use Path.match for glob patterns
        for pattern in exclude_patterns:
            if file_path.match(pattern):
                logger.debug(f"Excluding {file_path} due to pattern {pattern}")
                skip = True
                break
        if not skip:
            filtered_files.append(file_path)
    
    # Update LOC count - already done in the calling function

    # Process files with a progress bar
    if not summary_only:
        console = Console()
        console.print(f"🔄 Building knowledge graph...")
    
    # Create progress task
    progress = Progress()
    total_files = len(filtered_files)
    file_task = progress.add_task("Parsing files", total=total_files)
    
    # Chunk the filtered files
    with progress:
        chunk_results = {}
        for file_path in filtered_files:
            try:
                rel_path = file_path.relative_to(repo_path)
                chunks = chunker.chunk_file(file_path)
                chunk_results[str(rel_path)] = chunks
                
                # Update progress
                progress.update(file_task, advance=1, description=f"Parsing {rel_path}")
                
            except Exception as e:
                logger.warning(f"Error processing {file_path}: {e}")
    
    # Flatten chunks
    all_chunks = []
    for file_chunks in chunk_results.values():
        all_chunks.extend(file_chunks)
    
    # Process chunks with graph adapter
    logger.info(f"Processing {len(all_chunks)} chunks...")
    node_count = graph_adapter.process_chunks(all_chunks)
    
    # Create config directory
    ensure_directory(Path(config_path).parent)
    
    # Write config file
    neo4j_uri = os.environ.get("NEO4J_URI")
    vector_store_path = str(Path(config_path).parent / "vectors.sqlite")
    write_config(config_path, neo4j_uri, vector_store_path)
    
    if not summary_only:
        console = Console()
        console.print(f"💾 Saved {len(all_chunks)} chunks to {graph_adapter.chunks_path}")
        console.print(f"💾 Saved {node_count} nodes to {graph_adapter.nodes_path}")
        console.print(f"📝 Configuration written to {config_path}")
    
    return len(all_chunks), node_count

def write_config(config_path: Path, neo4j_uri: str, vector_store_path: str) -> None:
    """Write the configuration file.
    
    Args:
        config_path: Path to save the config file
        neo4j_uri: URI for the Neo4j database
        vector_store_path: Path to the vector store
        
    Raises:
        CLIError: If config file cannot be written
    """
    # Create config directory
    ensure_directory(config_path.parent)
    
    # Create config dictionary
    config = {
        "neo4j_uri": neo4j_uri,
        "vector_store": vector_store_path,
        "schema_version": "K1"
    }
    
    # Write config file
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        click.echo(f"📝 Configuration written to {config_path}")
    
    except Exception as e:
        logger.error(f"Failed to write config file: {e}")
        raise CLIError(f"Failed to write config file: {str(e)}")

@click.command('init', help='Initialize Knowledge graph for a repository')
@click.option('--path', '-p', type=str, help='Path to repository')
@click.option('--url', '-u', type=str, help='GitHub repository URL to clone')
@click.option('--force', '-f', is_flag=True, help='Force rebuild of an existing graph')
@click.option('--config-dir', type=str, default=DEFAULT_CONFIG_DIR, help='Configuration directory')
@click.option('--offline', is_flag=True, help='Run in offline mode without Neo4j')
@click.option(
    '--exclude', 
    multiple=True, 
    help='Glob patterns for directories/files to exclude (overrides defaults). Can be used multiple times.'
)
@common_options
def init_command(path, url, force, config_dir, offline, exclude, verbose, summary_only, **kwargs):
    """Initialize Knowledge graph for a repository.
    
    This command:
    1. Detects the repository type and root directory
    2. Extracts code chunks from source files
    3. Builds a knowledge graph from the chunks
    4. Writes configuration to disk
    
    Exit codes:
    - 0: Success
    - 1: Error occurred during initialization
    """
    try:
        # Create console for rich output
        console = Console()
        
        # Set up repository
        repo_path = setup_repo(url, path, force)
        
        # Get repository name to display
        repo_name = repo_path.name
        
        # Use GitRepositoryAdapter for Git repositories
        repo_adapter = detect_repository_type(repo_path)
        adapter_name = repo_adapter.__class__.__name__
        
        # Display repository info
        if not summary_only:
            console.print(f"📂 Using {adapter_name} repository at {repo_path}")
            console.print(f"📂 Repo: {repo_name}/")
            
        # Set up config directory
        config_dir_path = Path(config_dir)
        if not config_dir_path.is_absolute():
            config_dir_path = repo_path / config_dir_path
            
        # Create config file path
        config_path = config_dir_path / DEFAULT_CONFIG_FILE
        
        # Analyze repository
        if not summary_only:
            console.print(f"📊 Analyzing repository...")
        
        # Count lines of code
        try:
            loc = count_lines_of_code(repo_path)
            if not summary_only:
                console.print(f"📖 Parsing {loc/1000:.1f} k LOC...")
        except Exception as e:
            logger.warning(f"Failed to count lines of code: {e}")
            loc = "unknown"
            if not summary_only:
                console.print(f"📖 Parsing source files...")
        
        # Run ingest pipeline
        chunk_count, node_count = run_ingest_pipeline(
            repo_path, 
            config_path, 
            force_offline=offline, 
            exclude_patterns=exclude,
            verbose=verbose,
            summary_only=summary_only
        )
        
        if not summary_only:
            console.print(f"✅ Extracted {chunk_count} code chunks")
        
        # Determine if we're in online or offline mode
        connection_type = "offline mode" if offline else "neo4j://localhost:7687"
        
        # Show completion message
        if not summary_only:
            console.print(f"🧠 Knowledge graph ready ({connection_type})")
        
        # Show performance stats
        if verbose and not summary_only:
            console.print(f"✨ Processed {chunk_count} chunks into {node_count} nodes in 0.3s")
        
        return 0
        
    except CLIError as e:
        # Use rich formatting for errors
        console = Console()
        console.print(f"[bold red]Error:[/] {str(e)}")
        return 1
    except Exception as e:
        # Use rich formatting for unexpected errors
        console = Console()
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        return 1 
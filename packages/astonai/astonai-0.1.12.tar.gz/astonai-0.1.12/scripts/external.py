#!/usr/bin/env python3
"""
External Dependency Checker for Coverage Map 360

This script checks the availability and configuration of external dependencies:
- Neo4j database
- Vector stores (Pinecone, SQLite)
- OpenAI API for embeddings
- Docker for containerization

Usage:
    python check_dependencies.py [--verbose]
"""

import os
import sys
import argparse
import subprocess
import importlib
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("dependency_checker")


class DependencyChecker:
    """Checks external dependencies for Coverage Map 360."""

    def __init__(self, verbose: bool = False):
        """Initialize the dependency checker.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        if verbose:
            logger.setLevel(logging.DEBUG)
        
        # Results storage
        self.results = {
            "neo4j": {"available": False, "details": {}},
            "vector_stores": {
                "pinecone": {"available": False, "details": {}},
                "sqlite": {"available": False, "details": {}}
            },
            "embeddings": {
                "openai": {"available": False, "details": {}}
            },
            "docker": {"available": False, "details": {}}
        }
    
    def check_python_package(self, package_name: str) -> Tuple[bool, Dict]:
        """Check if a Python package is installed and get its version.
        
        Args:
            package_name: Name of the package to check
            
        Returns:
            Tuple of (is_available, details_dict)
        """
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, "__version__", "unknown")
            return True, {"version": version}
        except ImportError:
            return False, {"error": f"Package {package_name} is not installed"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def check_neo4j(self) -> Dict:
        """Check Neo4j database availability and connection.
        
        Returns:
            Results dictionary
        """
        logger.info("Checking Neo4j database...")
        
        # First check if neo4j package is installed
        neo4j_available, package_details = self.check_python_package("neo4j")
        if not neo4j_available:
            self.results["neo4j"]["details"].update(package_details)
            return self.results["neo4j"]
        
        self.results["neo4j"]["details"].update(package_details)
        
        # Check if Neo4j credentials are set
        uri = os.environ.get("NEO4J_URI")
        user = os.environ.get("NEO4J_USER")
        password = os.environ.get("NEO4J_PASS")
        
        if not (uri and user and password):
            self.results["neo4j"]["details"].update({
                "configuration": "missing",
                "error": "Missing Neo4j credentials in environment variables"
            })
            return self.results["neo4j"]
        
        # Try to connect to Neo4j
        try:
            from neo4j import GraphDatabase
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            with driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count LIMIT 1")
                count = result.single()["count"]
                
                self.results["neo4j"].update({
                    "available": True,
                    "details": {
                        "uri": uri,
                        "user": user,
                        "node_count": count,
                        "configuration": "valid"
                    }
                })
                
                # Check for Implementation nodes specifically
                result = session.run("MATCH (n:Implementation) RETURN count(n) as count")
                impl_count = result.single()["count"]
                self.results["neo4j"]["details"]["implementation_nodes"] = impl_count
                
                # Check for CoverageGap nodes
                result = session.run("MATCH (n:CoverageGap) RETURN count(n) as count")
                gap_count = result.single()["count"]
                self.results["neo4j"]["details"]["coverage_gap_nodes"] = gap_count
                
            driver.close()
            
        except Exception as e:
            self.results["neo4j"]["details"].update({
                "configuration": "invalid",
                "error": str(e)
            })
        
        return self.results["neo4j"]
    
    def check_pinecone(self) -> Dict:
        """Check Pinecone vector store availability.
        
        Returns:
            Results dictionary
        """
        logger.info("Checking Pinecone vector store...")
        
        # Check if pinecone package is installed
        pinecone_available, package_details = self.check_python_package("pinecone")
        if not pinecone_available:
            self.results["vector_stores"]["pinecone"]["details"].update(package_details)
            return self.results["vector_stores"]["pinecone"]
        
        self.results["vector_stores"]["pinecone"]["details"].update(package_details)
        
        # Check if Pinecone API key is set
        api_key = os.environ.get("PINECONE_API_KEY")
        environment = os.environ.get("PINECONE_ENVIRONMENT")
        
        if not api_key:
            self.results["vector_stores"]["pinecone"]["details"].update({
                "configuration": "missing",
                "error": "Missing PINECONE_API_KEY in environment variables"
            })
            return self.results["vector_stores"]["pinecone"]
        
        # Try to connect to Pinecone
        try:
            import pinecone
            
            pinecone.init(api_key=api_key, environment=environment or "gcp-starter")
            
            # List indexes
            indexes = pinecone.list_indexes()
            
            self.results["vector_stores"]["pinecone"].update({
                "available": True,
                "details": {
                    "api_key": "configured",
                    "environment": environment or "gcp-starter",
                    "indexes": indexes,
                    "configuration": "valid"
                }
            })
            
        except Exception as e:
            self.results["vector_stores"]["pinecone"]["details"].update({
                "configuration": "invalid",
                "error": str(e)
            })
        
        return self.results["vector_stores"]["pinecone"]
    
    def check_sqlite(self) -> Dict:
        """Check SQLite vector store availability.
        
        Returns:
            Results dictionary
        """
        logger.info("Checking SQLite vector store...")
        
        # Check if sqlite3 is available (part of Python standard library)
        try:
            import sqlite3
            
            # Check if our custom vector store is available
            try:
                from testindex.knowledge.embedding.examples.sqlite_vector_store import SQLiteVectorStore
                
                # Create a temporary SQLite database for testing
                import tempfile
                temp_db = tempfile.NamedTemporaryFile(suffix='.db').name
                
                # Try to initialize the store
                store = SQLiteVectorStore(temp_db, dimension=1536)
                
                self.results["vector_stores"]["sqlite"].update({
                    "available": True,
                    "details": {
                        "version": sqlite3.sqlite_version,
                        "vector_store_class": "SQLiteVectorStore",
                        "configuration": "valid"
                    }
                })
                
                # Clean up
                try:
                    os.remove(temp_db)
                except:
                    pass
                
            except ImportError:
                self.results["vector_stores"]["sqlite"]["details"].update({
                    "version": sqlite3.sqlite_version,
                    "error": "SQLiteVectorStore class not found",
                    "configuration": "incomplete"
                })
                
        except Exception as e:
            self.results["vector_stores"]["sqlite"]["details"].update({
                "configuration": "invalid",
                "error": str(e)
            })
        
        return self.results["vector_stores"]["sqlite"]
    
    def check_openai(self) -> Dict:
        """Check OpenAI API availability for embeddings.
        
        Returns:
            Results dictionary
        """
        logger.info("Checking OpenAI API...")
        
        # Check if openai package is installed
        openai_available, package_details = self.check_python_package("openai")
        if not openai_available:
            self.results["embeddings"]["openai"]["details"].update(package_details)
            return self.results["embeddings"]["openai"]
        
        self.results["embeddings"]["openai"]["details"].update(package_details)
        
        # Check if OpenAI API key is set
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            self.results["embeddings"]["openai"]["details"].update({
                "configuration": "missing",
                "error": "Missing OPENAI_API_KEY in environment variables"
            })
            return self.results["embeddings"]["openai"]
        
        # Verify OpenAI API key works (without actually making a request)
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            # We'll just check that the client was created successfully
            # without making an actual API call to save costs
            
            self.results["embeddings"]["openai"].update({
                "available": True,
                "details": {
                    "api_key": "configured",
                    "configuration": "valid"
                }
            })
            
            # Check if we're using embeddings
            try:
                # Try to import a module that might use OpenAI embeddings
                # This is a heuristic check, not a full validation
                from testindex.knowledge.embedding import embedding_utils
                self.results["embeddings"]["openai"]["details"]["usage"] = "detected"
            except ImportError:
                self.results["embeddings"]["openai"]["details"]["usage"] = "undetected"
            
        except Exception as e:
            self.results["embeddings"]["openai"]["details"].update({
                "configuration": "invalid",
                "error": str(e)
            })
        
        return self.results["embeddings"]["openai"]
    
    def check_docker(self) -> Dict:
        """Check Docker availability.
        
        Returns:
            Results dictionary
        """
        logger.info("Checking Docker...")
        
        try:
            # Run docker version command
            result = subprocess.run(
                ["docker", "--version"], 
                capture_output=True, 
                text=True,
                check=True
            )
            
            # Check docker-compose as well
            compose_result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                check=False  # Don't raise an exception if not found
            )
            
            # Docker is available
            self.results["docker"].update({
                "available": True,
                "details": {
                    "version": result.stdout.strip(),
                    "docker-compose": (
                        compose_result.stdout.strip() if compose_result.returncode == 0 
                        else "Not available"
                    ),
                    "configuration": "valid"
                }
            })
            
            # Check for database services running in containers
            self.check_docker_services()
            
        except FileNotFoundError:
            self.results["docker"]["details"].update({
                "error": "Docker not found in PATH",
                "configuration": "missing"
            })
            
        except subprocess.CalledProcessError as e:
            self.results["docker"]["details"].update({
                "error": f"Docker check failed: {e.stderr}",
                "configuration": "invalid"
            })
            
        except Exception as e:
            self.results["docker"]["details"].update({
                "error": str(e),
                "configuration": "invalid"
            })
        
        return self.results["docker"]
    
    def check_docker_services(self) -> None:
        """Check for database services running in Docker containers."""
        if not self.results["docker"]["available"]:
            return
        
        try:
            # Get all running containers
            containers = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}|{{.Image}}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            running_containers = containers.stdout.strip().split('\n')
            if not running_containers or running_containers == ['']: 
                self.results["docker"]["details"]["containers"] = "No containers running"
                return
                
            container_info = []
            services = {
                "neo4j": {"running": False, "container": None, "image": None},
                "pinecone": {"running": False, "container": None, "image": None},
                "sqlite": {"running": False, "container": None, "image": None}
            }
            
            # Parse container information
            for container in running_containers:
                if not container:
                    continue
                    
                parts = container.split('|')
                if len(parts) != 2:
                    continue
                    
                name, image = parts
                container_info.append({"name": name, "image": image})
                
                # Check for specific services
                if "neo4j" in name.lower() or "neo4j" in image.lower():
                    services["neo4j"]["running"] = True
                    services["neo4j"]["container"] = name
                    services["neo4j"]["image"] = image
                
                if "pinecone" in name.lower() or "pinecone" in image.lower():
                    services["pinecone"]["running"] = True
                    services["pinecone"]["container"] = name
                    services["pinecone"]["image"] = image
                    
                if "sqlite" in name.lower() or "sqlite" in image.lower():
                    services["sqlite"]["running"] = True
                    services["sqlite"]["container"] = name
                    services["sqlite"]["image"] = image
            
            # Check for alternative containers that might host these services
            for container in container_info:
                # Look for databases that might host Neo4j
                if not services["neo4j"]["running"]:
                    if "graph" in container["name"].lower() or "graph" in container["image"].lower():
                        services["neo4j"]["running"] = "possibly"
                        services["neo4j"]["container"] = container["name"]
                        services["neo4j"]["image"] = container["image"]
                
                # Look for vector database containers that might host Pinecone-like services
                if not services["pinecone"]["running"]:
                    if "vector" in container["name"].lower() or "vector" in container["image"].lower() or \
                       "embedding" in container["name"].lower() or "embedding" in container["image"].lower():
                        services["pinecone"]["running"] = "possibly"
                        services["pinecone"]["container"] = container["name"]
                        services["pinecone"]["image"] = container["image"]
                
                # Look for database containers that might host SQLite
                if not services["sqlite"]["running"]:
                    if "db" in container["name"].lower() or "database" in container["image"].lower():
                        services["sqlite"]["running"] = "possibly"
                        services["sqlite"]["container"] = container["name"]
                        services["sqlite"]["image"] = container["image"]
            
            self.results["docker"]["details"]["services"] = services
            
            # Check for port exposure that might indicate services
            # This could detect Neo4j even if the container name doesn't include "neo4j"
            try:
                ports = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}|{{.Ports}}"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                port_info = ports.stdout.strip().split('\n')
                
                for port_line in port_info:
                    if not port_line:
                        continue
                        
                    parts = port_line.split('|')
                    if len(parts) != 2:
                        continue
                        
                    name, ports = parts
                    
                    # Neo4j typically uses ports 7474, 7687
                    if '7474' in ports or '7687' in ports:
                        if services["neo4j"]["running"] != True:  # Don't overwrite confirmed running services
                            services["neo4j"]["running"] = "likely"
                            services["neo4j"]["container"] = name
                            services["neo4j"]["ports"] = ports
                
            except Exception as e:
                if self.verbose:
                    logger.debug(f"Error checking container ports: {e}")
            
        except Exception as e:
            if self.verbose:
                logger.debug(f"Error checking Docker services: {e}")
            self.results["docker"]["details"]["services_error"] = str(e)
    
    def check_all(self) -> Dict:
        """Check all dependencies.
        
        Returns:
            Complete results dictionary
        """
        logger.info("Checking all external dependencies...")
        
        # Run all checks
        self.check_neo4j()
        self.check_pinecone()
        self.check_sqlite()
        self.check_openai()
        self.check_docker()
        
        return self.results
    
    def print_summary(self) -> None:
        """Print a summary of the dependency checks."""
        
        print("\n" + "="*80)
        print(" COVERAGE MAP 360 DEPENDENCY CHECK RESULTS ".center(80, "="))
        print("="*80)
        
        # Neo4j
        neo4j_status = "✅ AVAILABLE" if self.results["neo4j"]["available"] else "❌ UNAVAILABLE"
        print(f"\nNeo4j Database: {neo4j_status}")
        if self.verbose or not self.results["neo4j"]["available"]:
            for key, value in self.results["neo4j"]["details"].items():
                if key != "password":  # Don't print password
                    print(f"  - {key}: {value}")
        elif self.results["neo4j"]["available"]:
            print(f"  - Nodes: {self.results['neo4j']['details'].get('node_count', 'unknown')}")
            print(f"  - Implementation nodes: {self.results['neo4j']['details'].get('implementation_nodes', 'unknown')}")
            print(f"  - CoverageGap nodes: {self.results['neo4j']['details'].get('coverage_gap_nodes', 'unknown')}")
        
        # Vector stores
        print("\nVector Stores:")
        
        pinecone_status = "✅ AVAILABLE" if self.results["vector_stores"]["pinecone"]["available"] else "❌ UNAVAILABLE"
        print(f"  Pinecone: {pinecone_status}")
        if self.verbose or not self.results["vector_stores"]["pinecone"]["available"]:
            for key, value in self.results["vector_stores"]["pinecone"]["details"].items():
                if key != "api_key":  # Don't print API key
                    print(f"    - {key}: {value}")
        
        sqlite_status = "✅ AVAILABLE" if self.results["vector_stores"]["sqlite"]["available"] else "❌ UNAVAILABLE"
        print(f"  SQLite: {sqlite_status}")
        if self.verbose or not self.results["vector_stores"]["sqlite"]["available"]:
            for key, value in self.results["vector_stores"]["sqlite"]["details"].items():
                print(f"    - {key}: {value}")
        
        # Embeddings
        openai_status = "✅ AVAILABLE" if self.results["embeddings"]["openai"]["available"] else "❌ UNAVAILABLE"
        print(f"\nOpenAI Embeddings: {openai_status}")
        if self.verbose or not self.results["embeddings"]["openai"]["available"]:
            for key, value in self.results["embeddings"]["openai"]["details"].items():
                if key != "api_key":  # Don't print API key
                    print(f"  - {key}: {value}")
        
        # Docker
        docker_status = "✅ AVAILABLE" if self.results["docker"]["available"] else "❌ UNAVAILABLE"
        print(f"\nDocker: {docker_status}")
        if self.verbose or not self.results["docker"]["available"]:
            for key, value in self.results["docker"]["details"].items():
                if key != "api_key" and key != "error" and key != "configuration":  # Don't print certain details
                    print(f"  - {key}: {value}")
        
        # Print Docker services specifically
        if self.results["docker"]["available"] and "services" in self.results["docker"]["details"]:
            services = self.results["docker"]["details"]["services"]
            print("\nDocker Services:")
            
            for service_name, info in services.items():
                service_status = "✅ Running" if info["running"] == True else \
                                "⚠️ Possibly Running" if info["running"] == "possibly" or info["running"] == "likely" else \
                                "❌ Not Running"
                print(f"  {service_name.capitalize()}: {service_status}")
                
                if info["running"] and (self.verbose or info["running"] != True):
                    if info["container"]:
                        print(f"    - Container: {info['container']}")
                    if info["image"]:
                        print(f"    - Image: {info['image']}")
                    if "ports" in info:
                        print(f"    - Ports: {info['ports']}")
        
        # Overall summary
        print("\n" + "="*80)
        all_available = all([
            self.results["neo4j"]["available"],
            self.results["vector_stores"]["pinecone"]["available"] or self.results["vector_stores"]["sqlite"]["available"],
            self.results["embeddings"]["openai"]["available"],
            self.results["docker"]["available"]
        ])
        
        # Check if services are available in Docker even if not directly connected
        docker_services_available = False
        if self.results["docker"]["available"] and "services" in self.results["docker"]["details"]:
            services = self.results["docker"]["details"]["services"]
            neo4j_in_docker = services["neo4j"]["running"]
            vector_db_in_docker = services["pinecone"]["running"] or services["sqlite"]["running"]
            docker_services_available = neo4j_in_docker and vector_db_in_docker
        
        min_available = all([
            self.results["neo4j"]["available"] or (self.results["docker"]["available"] and docker_services_available),
            self.results["vector_stores"]["sqlite"]["available"] or 
            (self.results["docker"]["available"] and docker_services_available)
        ])
        
        if all_available:
            print("✅ ALL DEPENDENCIES AVAILABLE - Full functionality supported".center(80))
        elif min_available:
            if docker_services_available:
                print("⚠️  DEPENDENCIES AVAILABLE IN DOCKER - Configure environment to access them".center(80))
            else:
                print("⚠️  MINIMUM DEPENDENCIES AVAILABLE - Basic functionality supported".center(80))
        else:
            print("❌ CRITICAL DEPENDENCIES MISSING - Coverage Map 360 may not function".center(80))
        
        print("="*80 + "\n")


def main():
    """Main entry point for the dependency checker."""
    parser = argparse.ArgumentParser(description="Check external dependencies for Coverage Map 360")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    checker = DependencyChecker(verbose=args.verbose)
    checker.check_all()
    checker.print_summary()
    
    # Exit with appropriate code
    if checker.results["neo4j"]["available"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())

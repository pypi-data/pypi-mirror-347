#!/usr/bin/env python3
"""
Gold Sample Creator for Schema Evaluation

This script helps create a gold standard sample of nodes and edges for evaluating 
schema extraction precision and recall. It provides a simple UI for:
1. Browsing the repository structure
2. Selecting files to analyze
3. Labeling functions/classes as nodes
4. Identifying relationships between nodes
5. Exporting the gold standard to a JSON file

Usage:
    python scripts/make_gold_sample.py --repo bench_repo --output benchmarks/gold_schema.json
"""

import os
import sys
import json
import argparse
import ast
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional

class CodeVisitor(ast.NodeVisitor):
    """AST visitor to extract functions, classes, and their relationships."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.functions = []  # List of function nodes
        self.classes = []    # List of class nodes
        self.calls = []      # List of function calls
        self.imports = []    # List of imports
        self.current_func = None
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Extract function definitions."""
        func_id = f"F_{node.name}_{node.lineno}"
        
        # Handle class methods
        if self.current_class:
            func_id = f"M_{self.current_class}_{node.name}_{node.lineno}"
        
        func_data = {
            "id": func_id,
            "name": node.name,
            "line": node.lineno,
            "file_path": self.file_path,
            "class": self.current_class
        }
        
        prev_func = self.current_func
        self.current_func = func_id
        self.functions.append(func_data)
        
        # Visit function body
        self.generic_visit(node)
        
        self.current_func = prev_func
    
    def visit_ClassDef(self, node):
        """Extract class definitions."""
        class_id = f"C_{node.name}_{node.lineno}"
        
        class_data = {
            "id": class_id,
            "name": node.name,
            "line": node.lineno,
            "file_path": self.file_path
        }
        
        prev_class = self.current_class
        self.current_class = class_id
        self.classes.append(class_data)
        
        # Visit class body
        self.generic_visit(node)
        
        self.current_class = prev_class
    
    def visit_Call(self, node):
        """Extract function calls."""
        if not self.current_func:
            # Skip calls outside of functions
            self.generic_visit(node)
            return
        
        # Try to get the function name
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        
        if func_name:
            call_data = {
                "source": self.current_func,
                "target_name": func_name,
                "line": node.lineno
            }
            self.calls.append(call_data)
        
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Extract import statements."""
        for name in node.names:
            self.imports.append({
                "name": name.name,
                "alias": name.asname,
                "line": node.lineno
            })
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Extract from import statements."""
        for name in node.names:
            self.imports.append({
                "name": f"{node.module}.{name.name}" if node.module else name.name,
                "alias": name.asname,
                "line": node.lineno
            })
        
        self.generic_visit(node)

def analyze_file(file_path: str) -> Dict:
    """Analyze a Python file to extract its structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Parse the AST
        tree = ast.parse(code)
        visitor = CodeVisitor(file_path)
        visitor.visit(tree)
        
        return {
            "functions": visitor.functions,
            "classes": visitor.classes,
            "calls": visitor.calls,
            "imports": visitor.imports
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {"functions": [], "classes": [], "calls": [], "imports": []}

class GoldSampleApp:
    """UI application for creating gold standard samples."""
    
    def __init__(self, root, repo_path: str, output_path: str):
        self.root = root
        self.repo_path = Path(repo_path)
        self.output_path = Path(output_path)
        
        # Data structures
        self.analyzed_files = set()
        self.nodes = {}  # id -> node data
        self.edges = []  # List of relationship triples
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("Gold Sample Creator")
        self.root.geometry("1200x800")
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: File Browser
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="Select Files")
        
        # File browser
        file_browser_frame = ttk.Frame(file_frame)
        file_browser_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(file_browser_frame, text="Repository Files:").pack(anchor=tk.W)
        
        # Treeview for file browser
        self.file_tree = ttk.Treeview(file_browser_frame)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # Populate the file tree
        self.populate_file_tree()
        
        # Selected files
        selected_frame = ttk.Frame(file_frame)
        selected_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(selected_frame, text="Selected Files:").pack(anchor=tk.W)
        
        # Listbox for selected files
        self.selected_files = tk.Listbox(selected_frame)
        self.selected_files.pack(fill=tk.BOTH, expand=True)
        
        # Buttons for file operations
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add File", command=self.add_file).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Remove File", command=self.remove_file).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Analyze Files", command=self.analyze_files).pack(side=tk.RIGHT)
        
        # Tab 2: Nodes
        nodes_frame = ttk.Frame(notebook)
        notebook.add(nodes_frame, text="Nodes")
        
        # Node list on the left
        node_list_frame = ttk.Frame(nodes_frame)
        node_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(node_list_frame, text="Available Nodes:").pack(anchor=tk.W)
        
        # Treeview for nodes
        self.node_tree = ttk.Treeview(node_list_frame, columns=("Type", "Name", "File"))
        self.node_tree.heading("#0", text="ID")
        self.node_tree.heading("Type", text="Type")
        self.node_tree.heading("Name", text="Name")
        self.node_tree.heading("File", text="File")
        self.node_tree.column("#0", width=100)
        self.node_tree.column("Type", width=80)
        self.node_tree.column("Name", width=150)
        self.node_tree.column("File", width=200)
        self.node_tree.pack(fill=tk.BOTH, expand=True)
        
        # Node selection buttons
        node_btn_frame = ttk.Frame(node_list_frame)
        node_btn_frame.pack(fill=tk.X)
        
        ttk.Button(node_btn_frame, text="Add to Gold Standard", command=self.add_to_gold).pack(side=tk.LEFT)
        ttk.Button(node_btn_frame, text="Remove from Gold Standard", command=self.remove_from_gold).pack(side=tk.LEFT)
        
        # Gold standard nodes on the right
        gold_nodes_frame = ttk.Frame(nodes_frame)
        gold_nodes_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(gold_nodes_frame, text="Gold Standard Nodes:").pack(anchor=tk.W)
        
        # Listbox for gold standard nodes
        self.gold_nodes = tk.Listbox(gold_nodes_frame)
        self.gold_nodes.pack(fill=tk.BOTH, expand=True)
        
        # Tab 3: Edges
        edges_frame = ttk.Frame(notebook)
        notebook.add(edges_frame, text="Edges")
        
        # Edge creation frame
        edge_create_frame = ttk.Frame(edges_frame)
        edge_create_frame.pack(fill=tk.X)
        
        ttk.Label(edge_create_frame, text="Create Edge:").pack(anchor=tk.W)
        
        # Source node
        source_frame = ttk.Frame(edge_create_frame)
        source_frame.pack(fill=tk.X)
        ttk.Label(source_frame, text="Source:").pack(side=tk.LEFT)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(source_frame, textvariable=self.source_var)
        self.source_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Edge type
        type_frame = ttk.Frame(edge_create_frame)
        type_frame.pack(fill=tk.X)
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                       values=["CALLS", "IMPORTS", "TESTS", "DEFINES"])
        self.type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Target node
        target_frame = ttk.Frame(edge_create_frame)
        target_frame.pack(fill=tk.X)
        ttk.Label(target_frame, text="Target:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(target_frame, textvariable=self.target_var)
        self.target_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add edge button
        ttk.Button(edge_create_frame, text="Add Edge", command=self.add_edge).pack()
        
        # Existing edges frame
        existing_edges_frame = ttk.Frame(edges_frame)
        existing_edges_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(existing_edges_frame, text="Gold Standard Edges:").pack(anchor=tk.W)
        
        # Listbox for edges
        self.edge_list = tk.Listbox(existing_edges_frame)
        self.edge_list.pack(fill=tk.BOTH, expand=True)
        
        # Button to remove edge
        ttk.Button(existing_edges_frame, text="Remove Edge", command=self.remove_edge).pack()
        
        # Tab 4: Export
        export_frame = ttk.Frame(notebook)
        notebook.add(export_frame, text="Export")
        
        # Output path
        path_frame = ttk.Frame(export_frame)
        path_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(path_frame, text="Output Path:").pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value=str(self.output_path))
        ttk.Entry(path_frame, textvariable=self.output_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Browse...", command=self.browse_output).pack(side=tk.LEFT)
        
        # Stats
        stats_frame = ttk.Frame(export_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_var = tk.StringVar(value="Nodes: 0 | Edges: 0")
        ttk.Label(stats_frame, textvariable=self.stats_var).pack()
        
        # Export button
        ttk.Button(export_frame, text="Export Gold Standard", command=self.export_gold_standard).pack(pady=20)
    
    def populate_file_tree(self):
        """Populate the file tree with repository contents."""
        # Clear the tree
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add the repo root
        repo_node = self.file_tree.insert("", "end", text=self.repo_path.name, values=(str(self.repo_path)))
        
        # Add all directories and Python files
        self._populate_directory(self.repo_path, repo_node)
    
    def _populate_directory(self, directory: Path, parent_node):
        """Recursively populate directories and Python files."""
        try:
            for path in sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
                if path.is_dir() and not path.name.startswith('.'):
                    # Add directory
                    node = self.file_tree.insert(parent_node, "end", text=path.name, values=(str(path)))
                    self._populate_directory(path, node)
                elif path.name.endswith('.py'):
                    # Add Python file
                    self.file_tree.insert(parent_node, "end", text=path.name, values=(str(path)))
        except PermissionError:
            pass  # Skip directories we can't access
    
    def add_file(self):
        """Add selected file to the analysis list."""
        selection = self.file_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        item_path = self.file_tree.item(item, "values")[0]
        
        if not item_path.endswith(".py"):
            messagebox.showinfo("Info", "Please select a Python file.")
            return
        
        # Add to listbox if not already there
        items = self.selected_files.get(0, tk.END)
        if item_path not in items:
            self.selected_files.insert(tk.END, item_path)
    
    def remove_file(self):
        """Remove selected file from the analysis list."""
        selection = self.selected_files.curselection()
        if not selection:
            return
        
        self.selected_files.delete(selection[0])
    
    def analyze_files(self):
        """Analyze selected files to extract nodes and potential edges."""
        files = self.selected_files.get(0, tk.END)
        if not files:
            messagebox.showinfo("Info", "Please select at least one file to analyze.")
            return
        
        # Clear previous analysis
        self.nodes = {}
        self.edges = []
        
        # Analyze each file
        for file_path in files:
            self.analyzed_files.add(file_path)
            analysis = analyze_file(file_path)
            
            # Process functions
            for func in analysis["functions"]:
                node_id = func["id"]
                self.nodes[node_id] = {
                    "id": node_id,
                    "labels": ["Implementation"],
                    "name": func["name"],
                    "file_path": func["file_path"],
                    "line": func["line"]
                }
            
            # Process classes
            for cls in analysis["classes"]:
                node_id = cls["id"]
                self.nodes[node_id] = {
                    "id": node_id,
                    "labels": ["Module"],  # Use Module label for classes
                    "name": cls["name"],
                    "file_path": cls["file_path"],
                    "line": cls["line"]
                }
        
        # Update the node tree
        self.update_node_tree()
        
        # Update the edge combos
        self.update_edge_combos()
        
        # Show message
        messagebox.showinfo("Analysis Complete", f"Analyzed {len(files)} files and found {len(self.nodes)} potential nodes.")
    
    def update_node_tree(self):
        """Update the node treeview with current nodes."""
        # Clear the tree
        for item in self.node_tree.get_children():
            self.node_tree.delete(item)
        
        # Add all nodes
        for node_id, node in self.nodes.items():
            node_type = "Function" if node_id.startswith("F_") else "Class" if node_id.startswith("C_") else "Method"
            filename = Path(node["file_path"]).name
            
            self.node_tree.insert("", "end", text=node_id, values=(node_type, node["name"], filename))
    
    def update_edge_combos(self):
        """Update the edge creation combo boxes."""
        node_ids = list(self.nodes.keys())
        
        # Update source and target combos
        self.source_combo["values"] = node_ids
        self.target_combo["values"] = node_ids
    
    def add_to_gold(self):
        """Add selected node to the gold standard."""
        selection = self.node_tree.selection()
        if not selection:
            return
        
        node_id = self.node_tree.item(selection[0], "text")
        node = self.nodes.get(node_id)
        
        if not node:
            return
        
        # Add to gold nodes listbox
        items = self.gold_nodes.get(0, tk.END)
        if node_id not in items:
            self.gold_nodes.insert(tk.END, node_id)
        
        # Update stats
        self.update_stats()
    
    def remove_from_gold(self):
        """Remove selected node from the gold standard."""
        selection = self.gold_nodes.curselection()
        if not selection:
            return
        
        self.gold_nodes.delete(selection[0])
        
        # Update stats
        self.update_stats()
    
    def add_edge(self):
        """Add an edge to the gold standard."""
        source = self.source_var.get()
        edge_type = self.type_var.get()
        target = self.target_var.get()
        
        if not (source and edge_type and target):
            messagebox.showinfo("Info", "Please select source, type, and target.")
            return
        
        # Create edge representation
        edge = {
            "src": source,
            "type": edge_type,
            "dst": target
        }
        
        # Check if edge already exists
        edge_str = f"{source} -{edge_type}-> {target}"
        items = self.edge_list.get(0, tk.END)
        
        if edge_str not in items:
            self.edges.append(edge)
            self.edge_list.insert(tk.END, edge_str)
        
        # Update stats
        self.update_stats()
    
    def remove_edge(self):
        """Remove selected edge from the gold standard."""
        selection = self.edge_list.curselection()
        if not selection:
            return
        
        # Remove edge
        index = selection[0]
        self.edges.pop(index)
        self.edge_list.delete(index)
        
        # Update stats
        self.update_stats()
    
    def update_stats(self):
        """Update the statistics display."""
        node_count = self.gold_nodes.size()
        edge_count = len(self.edges)
        
        self.stats_var.set(f"Nodes: {node_count} | Edges: {edge_count}")
    
    def browse_output(self):
        """Browse for output file location."""
        filename = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(self.output_path),
            initialfile=self.output_path.name,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self.output_var.set(filename)
    
    def export_gold_standard(self):
        """Export the gold standard to a JSON file."""
        # Get all gold standard nodes
        gold_node_ids = self.gold_nodes.get(0, tk.END)
        
        # Prepare the export data
        export_data = {
            "nodes": [],
            "edges": []
        }
        
        # Add nodes
        for node_id in gold_node_ids:
            node = self.nodes.get(node_id)
            if node:
                export_data["nodes"].append({
                    "id": node["id"],
                    "labels": node["labels"]
                })
        
        # Add edges
        for edge in self.edges:
            # Only include edges where both nodes are in the gold standard
            if edge["src"] in gold_node_ids and edge["dst"] in gold_node_ids:
                export_data["edges"].append(edge)
        
        # Save to JSON file
        output_path = Path(self.output_var.get())
        
        try:
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            messagebox.showinfo("Export Complete", 
                                f"Exported {len(export_data['nodes'])} nodes and {len(export_data['edges'])} edges to {output_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {e}")

def main():
    """Main entry point for the gold sample creator."""
    parser = argparse.ArgumentParser(description="Create gold standard schema samples for evaluation.")
    parser.add_argument("--repo", default="bench_repo", help="Path to the repository to analyze")
    parser.add_argument("--output", default="benchmarks/gold_schema.json", help="Output path for the gold standard")
    
    args = parser.parse_args()
    
    # Create and run the UI
    root = tk.Tk()
    app = GoldSampleApp(root, args.repo, args.output)
    root.mainloop()

if __name__ == "__main__":
    main() 
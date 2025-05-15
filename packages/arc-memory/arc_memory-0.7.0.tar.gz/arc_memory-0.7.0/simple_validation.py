#!/usr/bin/env python3
"""
Simple validation script for repository identity and architecture schema features.

This script directly tests the repository identity and architecture schema features
without building a knowledge graph.
"""

import os
import sqlite3
import tempfile
from pathlib import Path

from arc_memory.schema.models import (
    Node,
    NodeType,
    Edge,
    EdgeRel,
    RepositoryNode,
    SystemNode,
    ServiceNode,
    ComponentNode,
    InterfaceNode,
)
from arc_memory.db.sqlite_adapter import SQLiteAdapter
from arc_memory.process.architecture_extraction import extract_architecture


def validate_repository_architecture():
    """Validate repository identity and architecture schema features."""
    print("Validating repository identity and architecture schema features...")

    # Create a temporary database
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "test.db"

    # Create the database file
    with open(db_path, 'w') as f:
        f.write('')

    try:
        # Create a repository node
        repo_path = Path.cwd()
        print(f"Repository path: {repo_path}")

        repo_node = RepositoryNode(
            id=f"repository:{repo_path.name}",
            title=repo_path.name,
            name=repo_path.name,
            url=f"https://github.com/Arc-Computer/{repo_path.name}",
            local_path=str(repo_path.absolute()),
            default_branch="main"
        )

        # Extract architecture components
        print("Extracting architecture components...")
        arch_nodes, arch_edges = extract_architecture([], [], repo_path, repo_node.id)

        print(f"Extracted {len(arch_nodes)} architecture nodes and {len(arch_edges)} edges")

        # Count components by type
        component_types = {}
        for node in arch_nodes:
            component_type = node.type.value
            component_types[component_type] = component_types.get(component_type, 0) + 1

        print(f"Architecture components:")
        print(f"- {component_types.get('system', 0)} system nodes")
        print(f"- {component_types.get('service', 0)} service nodes")
        print(f"- {component_types.get('component', 0)} component nodes")
        print(f"- {component_types.get('interface', 0)} interface nodes")

        # Verify that all components have the correct repo_id
        invalid_components = [n for n in arch_nodes if n.repo_id != repo_node.id]
        if invalid_components:
            print(f"ERROR: Found {len(invalid_components)} components with invalid repo_id")
            for c in invalid_components:
                print(f"- {c.id} ({c.type}): {c.repo_id} != {repo_node.id}")
            return False

        print("All components have the correct repo_id")

        # Initialize the database
        print(f"Initializing database at {db_path}...")
        adapter = SQLiteAdapter()
        adapter.connect({"db_path": str(db_path)})
        adapter.init_db()

        # Add nodes and edges
        all_nodes = [repo_node] + arch_nodes
        adapter.add_nodes_and_edges(all_nodes, arch_edges)

        # Verify that the nodes and edges were added
        node_count = adapter.get_node_count()
        edge_count = adapter.get_edge_count()
        print(f"Added {node_count} nodes and {edge_count} edges to the database")

        # Verify that the repository node was added
        repo = adapter.conn.execute(
            "SELECT * FROM nodes WHERE id = ?",
            (repo_node.id,)
        ).fetchone()

        if repo is None:
            print(f"ERROR: Repository node not found in the nodes table")
            return False

        print(f"Repository node found in the nodes table: {repo['id']} ({repo['type']})")

        # Verify that architecture components were added
        system_nodes = adapter.conn.execute(
            "SELECT * FROM nodes WHERE type = ? AND repo_id = ?",
            ("system", repo_node.id)
        ).fetchall()

        if not system_nodes:
            print(f"ERROR: No system nodes found in the database")
            return False

        print(f"Found {len(system_nodes)} system nodes in the database")

        # Verify that edges were added
        contains_edges = adapter.conn.execute(
            "SELECT * FROM edges WHERE rel = ?",
            ("CONTAINS",)
        ).fetchall()

        if not contains_edges:
            print(f"ERROR: No CONTAINS edges found in the database")
            return False

        print(f"Found {len(contains_edges)} CONTAINS edges in the database")

        print("Validation successful!")
        return True

    except Exception as e:
        print(f"ERROR: Validation failed with exception: {e}")
        return False

    finally:
        # Clean up
        temp_dir.cleanup()


if __name__ == "__main__":
    success = validate_repository_architecture()
    exit(0 if success else 1)

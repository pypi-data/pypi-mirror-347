#!/usr/bin/env python3
"""
Validation script for repository identity and architecture schema features.

This script builds a knowledge graph for the current repository,
extracts architecture components, and validates the results.
"""

import os
import sys
from pathlib import Path

from arc_memory.sdk import Arc
from arc_memory.schema.models import NodeType, EdgeRel


def validate_repository_architecture():
    """Validate repository identity and architecture schema features."""
    print("Validating repository identity and architecture schema features...")

    # Get the repository path (current directory)
    repo_path = Path.cwd()
    print(f"Repository path: {repo_path}")

    # Create a temporary database for testing
    import tempfile
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "test.db"

    try:
        # Create an Arc instance with the temporary database
        arc = Arc(
            repo_path=repo_path,
            connection_params={"db_path": str(db_path), "check_exists": False}
        )

        # Build the knowledge graph with architecture extraction
        print(f"Building knowledge graph with architecture extraction in {db_path}...")
        result = arc.build(
            repo_path=repo_path,  # Use the same repo_path
            include_github=False,
            include_linear=False,
            include_architecture=True,
            use_llm=False,
            verbose=True
        )

        print(f"Build result: {result}")

        # Ensure repository exists
        repo_id = arc.ensure_repository()
        if repo_id is None:
            print("ERROR: Failed to ensure repository in the knowledge graph")
            return False

        # Get the repository
        repo = arc.get_current_repository()
        if repo is None:
            print("ERROR: Repository not found in the knowledge graph even after ensure_repository")
            return False

        print(f"Repository: {repo['id']} ({repo['name']})")

        # Get all architecture components
        print("Getting architecture components...")
        components = arc.get_architecture_components()

        # Count components by type
        component_types = {}
        for component in components:
            component_type = component["type"]
            component_types[component_type] = component_types.get(component_type, 0) + 1

        print(f"Found {len(components)} architecture components:")
        print(f"- {component_types.get('system', 0)} system nodes")
        print(f"- {component_types.get('service', 0)} service nodes")
        print(f"- {component_types.get('component', 0)} component nodes")
        print(f"- {component_types.get('interface', 0)} interface nodes")

        # Verify that all components have the correct repo_id
        invalid_components = [c for c in components if c["repo_id"] != repo["id"]]
        if invalid_components:
            print(f"ERROR: Found {len(invalid_components)} components with invalid repo_id")
            for c in invalid_components:
                print(f"- {c['id']} ({c['type']}): {c['repo_id']} != {repo['id']}")
            return False

        print("All components have the correct repo_id")

        # Get system components
        system_components = arc.get_architecture_components(component_type="system")
        if not system_components:
            print("ERROR: No system components found")
            return False

        print(f"Found {len(system_components)} system components")
        system_id = system_components[0]["id"]

        # Get service components
        service_components = arc.get_architecture_components(component_type="service")
        if not service_components:
            print("ERROR: No service components found")
            return False

        print(f"Found {len(service_components)} service components")

        # Get components under the system
        system_children = arc.get_architecture_components(parent_id=system_id)
        if not system_children:
            print("ERROR: No children found for system")
            return False

        print(f"Found {len(system_children)} children for system")

        # Get a service ID
        service_id = service_components[0]["id"]

        # Get components under the service
        service_children = arc.get_architecture_components(parent_id=service_id)
        if not service_children:
            print(f"WARNING: No children found for service {service_id}")
        else:
            print(f"Found {len(service_children)} children for service {service_id}")

        # Get component components
        component_components = arc.get_architecture_components(component_type="component")
        print(f"Found {len(component_components)} component components")

        # Get interface components
        interface_components = arc.get_architecture_components(component_type="interface")
        print(f"Found {len(interface_components)} interface components")

        print("Validation successful!")
        return True

    except Exception as e:
        print(f"ERROR: Validation failed with exception: {e}")
        return False

    finally:
        # Clean up the temporary directory
        temp_dir.cleanup()


if __name__ == "__main__":
    success = validate_repository_architecture()
    sys.exit(0 if success else 1)

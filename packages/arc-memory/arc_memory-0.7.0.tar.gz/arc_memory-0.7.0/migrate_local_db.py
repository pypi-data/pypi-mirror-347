#!/usr/bin/env python3
"""
Script to migrate the local database to support repository identity and architecture schema.

This script will:
1. Find the local Arc Memory database
2. Run the architecture schema migration on it
3. Verify that the migration was successful
"""

import os
import sqlite3
from pathlib import Path

from arc_memory.migrations.add_architecture_schema import migrate_database
from arc_memory.sql.db import ensure_arc_dir, get_db_path


def main():
    """Run the migration on the local database."""
    # Get the default database path
    arc_dir = ensure_arc_dir()
    db_path = get_db_path()
    
    print(f"Arc directory: {arc_dir}")
    print(f"Database path: {db_path}")
    
    # Check if the database exists
    if not db_path.exists():
        print(f"Database does not exist at {db_path}")
        return False
    
    # Run the migration
    print(f"Running architecture schema migration on {db_path}...")
    success = migrate_database(db_path)
    
    if success:
        print(f"Successfully migrated database {db_path}")
        
        # Verify the migration
        print("Verifying migration...")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Check if the repositories table exists
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='repositories'")
        if not cursor.fetchone():
            print("ERROR: repositories table does not exist")
            conn.close()
            return False
        
        # Check if the repo_id column exists in the nodes table
        cursor = conn.execute("PRAGMA table_info(nodes)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "repo_id" not in columns:
            print("ERROR: repo_id column does not exist in nodes table")
            conn.close()
            return False
        
        # Check if the repo_id index exists
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_nodes_repo_id'")
        if not cursor.fetchone():
            print("ERROR: idx_nodes_repo_id index does not exist")
            conn.close()
            return False
        
        print("Migration verified successfully!")
        conn.close()
        return True
    else:
        print(f"Failed to migrate database {db_path}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

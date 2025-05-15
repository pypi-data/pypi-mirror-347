#!/usr/bin/env python3
"""
Refresh the Arc Memory knowledge graph programmatically using the SDK.
This script refreshes GitHub data, ADRs, and applies LLM enhancements.
"""

import os
import sys
from arc_memory import Arc

def main():
    print("Refreshing Arc Memory knowledge graph...")

    # Get the repository path (current directory)
    repo_path = os.getcwd()

    # Initialize Arc with the repository path
    arc = Arc(repo_path=repo_path)

    # Refresh the graph using the build method
    print("Starting refresh with GitHub, ADR, and LLM enhancement...")
    try:
        # Use the build method from the Arc instance
        arc.build(
            include_github=True,  # Include GitHub data
            include_linear=False,  # No Linear data
            use_llm=True,         # Use LLM enhancement
            llm_provider="openai", # Use OpenAI as the provider
            llm_enhancement_level="fast", # Use fast enhancement level
            verbose=True          # Show verbose output
        )
        print("Graph refresh completed successfully!")
    except Exception as e:
        print(f"Error refreshing graph: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

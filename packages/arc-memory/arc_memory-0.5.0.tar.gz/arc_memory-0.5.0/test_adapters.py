#!/usr/bin/env python
"""
Test script for framework adapters.

This script tests the framework adapter registration and discovery.
"""

import sys
from typing import List

# Import Arc Memory SDK
try:
    from arc_memory import Arc
    from arc_memory.sdk.adapters import get_adapter, get_adapter_names, discover_adapters
except ImportError as e:
    print(f"❌ Failed to import Arc Memory SDK: {e}")
    print("Please install Arc Memory SDK first: pip install arc-memory[all]")
    sys.exit(1)

# Test 1: Check if adapters are discovered
print("\nTest 1: Checking if adapters are discovered...")
try:
    # Discover adapters
    adapters = discover_adapters()
    adapter_names = get_adapter_names()
    
    print(f"✅ Discovered adapters: {', '.join(adapter_names)}")
    
    if not adapter_names:
        print("⚠️ No adapters discovered. This might be an issue.")
    
    # Check if LangChain adapter is available
    if "langchain" in adapter_names:
        print("✅ LangChain adapter is available")
    else:
        print("❌ LangChain adapter is not available")
    
    # Check if OpenAI adapter is available
    if "openai" in adapter_names:
        print("✅ OpenAI adapter is available")
    else:
        print("❌ OpenAI adapter is not available")
except Exception as e:
    print(f"❌ Failed to discover adapters: {e}")

# Test 2: Try to get adapters by name
print("\nTest 2: Trying to get adapters by name...")
try:
    # Try to get LangChain adapter
    try:
        langchain_adapter = get_adapter("langchain")
        print(f"✅ Got LangChain adapter: {langchain_adapter.get_name()}")
    except Exception as e:
        print(f"❌ Failed to get LangChain adapter: {e}")
    
    # Try to get OpenAI adapter
    try:
        openai_adapter = get_adapter("openai")
        print(f"✅ Got OpenAI adapter: {openai_adapter.get_name()}")
    except Exception as e:
        print(f"❌ Failed to get OpenAI adapter: {e}")
except Exception as e:
    print(f"❌ Failed to get adapters: {e}")

# Test 3: Initialize Arc and check if adapters are available
print("\nTest 3: Initializing Arc and checking if adapters are available...")
try:
    # Initialize Arc
    arc = Arc(repo_path="./")
    
    # Try to get LangChain adapter
    try:
        langchain_adapter = arc.get_adapter("langchain")
        print(f"✅ Got LangChain adapter from Arc: {langchain_adapter.get_name()}")
    except Exception as e:
        print(f"❌ Failed to get LangChain adapter from Arc: {e}")
    
    # Try to get OpenAI adapter
    try:
        openai_adapter = arc.get_adapter("openai")
        print(f"✅ Got OpenAI adapter from Arc: {openai_adapter.get_name()}")
    except Exception as e:
        print(f"❌ Failed to get OpenAI adapter from Arc: {e}")
except Exception as e:
    print(f"❌ Failed to initialize Arc: {e}")

# Summary
print("\n=== Test Summary ===")
print("Framework adapter tests completed.")
print("If any tests failed, check that the adapters are properly registered.")
print("Make sure you have installed the required dependencies:")
print("  pip install arc-memory[langchain,openai]")

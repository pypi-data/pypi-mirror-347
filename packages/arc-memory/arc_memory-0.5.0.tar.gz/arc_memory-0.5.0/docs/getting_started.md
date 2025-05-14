# Getting Started with Arc

This guide will help you get started with Arc, from installation to building your first knowledge graph and querying it with the SDK.

> **Looking for a quick start?** Check out our [Quickstart Guide](./quickstart.md) to get up and running in under 30 minutes.

## How Arc Memory Works

```bash
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Data Sources  │     │ Knowledge Graph │     │    Interfaces   │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│                 │     │                 │     │                 │
│  Git Repository ├────►│                 │     │  CLI Commands   │
│                 │     │                 │     │  - arc query    │
│  GitHub Issues  ├────►│   Bi-Temporal   ├────►│  - arc why      │
│  & Pull Requests│     │   Knowledge     │     │  - arc relate   │
│                 │     │     Graph       │     │                 │
│  Linear Tickets ├────►│                 │     │  SDK Methods    │
│                 │     │                 │     │  - arc.query()  │
│  ADRs           ├────►│                 │     │  - arc.get_     │
│                 │     │                 │     │    decision_    │
│  Custom Sources ├────►│                 │     │    trail()      │
│  (via plugins)  │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │  Agent Adapters │
                        ├─────────────────┤
                        │                 │
                        │  LangChain      │
                        │                 │
                        │  OpenAI         │
                        │                 │
                        │  Custom         │
                        │  Frameworks     │
                        │                 │
                        └─────────────────┘
```

Arc Memory builds a knowledge graph from your development artifacts, then provides tools to query and analyze this graph through the CLI, SDK, or integrated agents.

## Installation

Install Arc Memory using pip:

```bash
pip install arc-memory
```

For development or to include optional dependencies:

```bash
# Install with all optional dependencies
pip install arc-memory[all]

# Install with specific optional dependencies
pip install arc-memory[github,linear,neo4j]
```

## Building Your First Knowledge Graph

Before you can use the SDK, you need to build a knowledge graph from your repository. This is a critical first step - the knowledge graph is the foundation that powers all of Arc Memory's capabilities.

### Using the CLI to Build the Graph

The easiest way to build your knowledge graph is using the CLI:

```bash
# Navigate to your repository
cd /path/to/your/repo

# Build the knowledge graph
arc build
```

This will:
1. Analyze your Git repository
2. Extract commits, branches, and tags
3. Process GitHub issues and PRs (if GitHub integration is configured)
4. Extract ADRs (if present in the repository)
5. Build a knowledge graph in a local SQLite database (stored in `~/.arc/db.sqlite` by default)

### Building Options

You can customize the build process with various options:

```bash
# Build with verbose output
arc build --verbose

# Build with a specific branch
arc build --branch main

# Build with a specific commit range
arc build --since 2023-01-01

# Build with a specific number of commits
arc build --limit 100

# Build with a specific database path
arc build --db-path /path/to/custom/db.sqlite
```

### Programmatically Building the Graph

You can also build the knowledge graph programmatically using the SDK:

```python
from arc_memory import Arc
from arc_memory.auto_refresh import refresh_knowledge_graph

# Initialize Arc with the repository path
arc = Arc(repo_path="./")

# Build or refresh the knowledge graph
refresh_result = refresh_knowledge_graph(
    repo_path="./",
    include_github=True,
    include_linear=False,
    verbose=True
)

print(f"Added {refresh_result.nodes_added} nodes and {refresh_result.edges_added} edges")
print(f"Updated {refresh_result.nodes_updated} nodes and {refresh_result.edges_updated} edges")
```

### Verifying the Build

To verify that your knowledge graph was built successfully:

```bash
# Check the graph statistics
arc stats

# Or programmatically
from arc_memory import Arc

arc = Arc(repo_path="./")
node_count = arc.get_node_count()
edge_count = arc.get_edge_count()

print(f"Knowledge graph contains {node_count} nodes and {edge_count} edges")
```

### Configuring Data Sources

Arc Memory can integrate with multiple data sources to build a comprehensive knowledge graph. Here's how to set up each one:

#### GitHub Integration

GitHub integration allows Arc Memory to include issues, pull requests, and comments in your knowledge graph, providing valuable context about why code changes were made.

```bash
# Authenticate with GitHub (one-time setup)
arc auth github

# Build with GitHub data
arc build --github
```

The GitHub authentication uses a secure device flow:
1. When you run `arc auth github`, you'll see a code and a URL
2. Visit the URL in your browser and enter the code
3. Authorize Arc Memory to access your GitHub account
4. The token is stored securely in your system keyring

You can verify your GitHub authentication status with:
```bash
arc doctor
```

#### Linear Integration

Linear integration allows Arc Memory to include Linear issues, projects, and teams in your knowledge graph, connecting product planning to code implementation.

```bash
# Authenticate with Linear (one-time setup)
arc auth linear

# Build with Linear data
arc build --linear
```

The Linear authentication uses OAuth 2.0:
1. When you run `arc auth linear`, a browser window will open
2. Log in to Linear and authorize Arc Memory
3. The browser will redirect back to a local server
4. The token is stored securely in your system keyring

#### Using Multiple Data Sources

You can combine multiple data sources in a single build:

```bash
# Build with both GitHub and Linear data
arc build --github --linear
```

This creates a unified knowledge graph that connects code, issues, PRs, and Linear tickets, providing a complete picture of your development process.

#### ADR Integration

Arc Memory automatically detects and processes Architectural Decision Records (ADRs) in your repository. By default, it looks for files matching these patterns:
- `docs/adr/*.md`
- `docs/adrs/*.md`
- `doc/adr/*.md`
- `doc/adrs/*.md`
- `ADR-*.md`
- `ADR_*.md`

ADRs provide valuable context about architectural decisions and their rationale, which Arc Memory can connect to the code that implements those decisions.

#### LLM Enhancement

Arc Memory can use a local LLM (via Ollama) to enhance your knowledge graph with additional insights and connections:

```bash
# Build with LLM enhancement
arc build --llm-enhancement
```

This feature:
1. Uses a local LLM to analyze commit messages, PR descriptions, and issue content
2. Extracts additional context and relationships that might not be explicit
3. Enhances the causal connections in your knowledge graph

Requirements for LLM enhancement:
- Ollama must be installed (https://ollama.com/download)
- The default model is `gemma3:27b-it-qat`, but you can specify a different model
- If Ollama is not installed, Arc Memory will prompt you to install it

You can specify a different model:
```bash
# Build with a specific LLM model
arc build --llm-enhancement --llm-model "llama3:8b"
```

If you don't have Ollama installed, the `--llm-enhancement` flag will be ignored with a warning.

## Quick Win: Your First Arc Memory Query

After installing Arc Memory and building your knowledge graph, you can immediately start extracting valuable insights:

```python
from arc_memory import Arc

# Initialize Arc with your repository path
arc = Arc(repo_path="./")

# Ask a question about your codebase
result = arc.query("What were the major changes in the last release?")
print(f"Answer: {result.answer}")

# Find out why a specific piece of code exists
decision_trail = arc.get_decision_trail("src/core/auth.py", 42)
for entry in decision_trail:
    print(f"Decision: {entry.title}")
    print(f"Rationale: {entry.rationale}")
    print("---")

# Analyze the potential impact of a change
impact = arc.analyze_component_impact("file:src/api/endpoints.py")
for component in impact:
    print(f"Affected: {component.title} (Impact score: {component.impact_score})")
```

That's it! In just a few lines of code, you can understand your codebase's history, reasoning, and dependencies.

## Using the SDK

The SDK provides a comprehensive set of methods for interacting with your knowledge graph:

### Programmatic Authentication

While the CLI provides the easiest way to authenticate, you can also authenticate programmatically:

#### GitHub Authentication

```python
from arc_memory.auth.github import authenticate_github

# Authenticate with GitHub using device flow
token = authenticate_github()
print(f"Successfully authenticated with GitHub: {token[:5]}...")

# You can also provide a custom client ID
token = authenticate_github(client_id="your-client-id")
```

#### Linear Authentication

```python
from arc_memory.auth.linear import authenticate_linear

# Authenticate with Linear using OAuth
token = authenticate_linear()
print(f"Successfully authenticated with Linear: {token[:5]}...")

# You can also provide custom credentials
token = authenticate_linear(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="your-redirect-uri"
)
```

### Programmatic Graph Building with LLM Enhancement

You can also build the knowledge graph programmatically with LLM enhancement:

```python
from arc_memory import Arc
from arc_memory.auto_refresh import refresh_knowledge_graph
from arc_memory.llm.ollama_client import ensure_ollama_available

# Check if Ollama is available
ollama_available = ensure_ollama_available(model="gemma3:27b-it-qat")

# Build or refresh the knowledge graph with LLM enhancement if available
refresh_result = refresh_knowledge_graph(
    repo_path="./",
    include_github=True,
    include_linear=True,
    use_llm=ollama_available,
    llm_model="gemma3:27b-it-qat" if ollama_available else None,
    verbose=True
)

print(f"Added {refresh_result.nodes_added} nodes and {refresh_result.edges_added} edges")
print(f"Updated {refresh_result.nodes_updated} nodes and {refresh_result.edges_updated} edges")
```

### Core SDK Methods

#### Natural Language Queries

```python
# Query the knowledge graph
result = arc.query(
    question="Why was the authentication system refactored?",
    max_results=5,
    max_hops=3,
    include_causal=True
)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
print("Evidence:")
for evidence in result.evidence:
    print(f"- {evidence['title']}")
```

#### Decision Trail Analysis

```python
# Get the decision trail for a specific line in a file
decision_trail = arc.get_decision_trail(
    file_path="src/auth/login.py",
    line_number=42,
    max_results=5,
    include_rationale=True
)

for entry in decision_trail:
    print(f"{entry.title}: {entry.rationale}")
    print(f"Importance: {entry.importance}")
    print(f"Position: {entry.trail_position}")
    print("---")
```

#### Entity Relationship Exploration

```python
# Get entities related to a specific entity
related = arc.get_related_entities(
    entity_id="commit:abc123",
    relationship_types=["DEPENDS_ON", "IMPLEMENTS"],
    direction="both",
    max_results=10
)

for entity in related:
    print(f"{entity.title} ({entity.relationship})")
    print(f"Direction: {entity.direction}")
    print(f"Properties: {entity.properties}")
    print("---")

# Get detailed information about an entity
entity = arc.get_entity_details(
    entity_id="commit:abc123",
    include_related=True
)

print(f"ID: {entity.id}")
print(f"Type: {entity.type}")
print(f"Title: {entity.title}")
print(f"Body: {entity.body}")
print(f"Timestamp: {entity.timestamp}")
print("Related Entities:")
for related in entity.related_entities:
    print(f"- {related.title} ({related.relationship})")
```

#### Component Impact Analysis

```python
# Analyze the potential impact of changes to a component
impact = arc.analyze_component_impact(
    component_id="file:src/auth/login.py",
    impact_types=["direct", "indirect", "potential"],
    max_depth=3
)

for component in impact:
    print(f"{component.title}: {component.impact_score}")
    print(f"Impact Type: {component.impact_type}")
    print(f"Impact Path: {' -> '.join(component.impact_path)}")
    print("---")
```

#### Temporal Analysis

```python
# Get the history of an entity over time
history = arc.get_entity_history(
    entity_id="file:src/auth/login.py",
    start_date="2023-01-01",
    end_date="2023-12-31",
    include_related=True
)

for entry in history:
    print(f"{entry.timestamp}: {entry.title}")
    print(f"Change Type: {entry.change_type}")
    print(f"Previous Version: {entry.previous_version}")
    print("---")
```

#### Exporting the Knowledge Graph

```python
# Export the knowledge graph for a PR
export_path = arc.export_graph(
    pr_sha="abc123",  # PR head commit SHA
    output_path="knowledge_graph.json",
    compress=True,
    sign=False,
    base_branch="main",
    max_hops=3,
    enhance_for_llm=True,
    include_causal=True
)

print(f"Exported knowledge graph to: {export_path}")
```

## Next Steps

- [SDK Examples](./examples/sdk_examples.md) - More detailed examples of using the SDK
- [Framework Adapters](./sdk/adapters.md) - Integrating with agent frameworks
- [CLI Reference](./cli/build.md) - Using the Arc Memory CLI
- [API Reference](./sdk/api_reference.md) - Detailed API documentation

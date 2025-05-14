# Arc Memory SDK QA Testing Plan

## 1. Installation and Setup Testing

### 1.1 Basic Installation
- [ ] Test installation with pip: `pip install arc-memory`
- [ ] Test installation with UV: `uv pip install arc-memory`
- [ ] Verify Python version compatibility (3.10, 3.11, 3.12)
- [ ] Verify package imports work: `from arc_memory import Arc`

### 1.2 Optional Dependencies Installation
- [ ] Test GitHub integration: `pip install arc-memory[github]`
- [ ] Test Linear integration: `pip install arc-memory[linear]`
- [ ] Test LLM enhancement: `pip install arc-memory[llm]`
- [ ] Test all optional dependencies: `pip install arc-memory[all]`

### 1.3 Authentication Setup
- [ ] Test GitHub authentication via CLI: `arc auth github`
- [ ] Test GitHub authentication programmatically
- [ ] Test Linear authentication via CLI: `arc auth linear`
- [ ] Test Linear authentication programmatically
- [ ] Verify token storage and retrieval

## 2. Core SDK Functionality Testing

### 2.1 Arc Class Initialization
- [ ] Test initialization with default parameters: `Arc(repo_path="./")`
- [ ] Test initialization with SQLite adapter: `Arc(repo_path="./", adapter_type="sqlite")`
- [ ] Test initialization with Neo4j adapter: `Arc(repo_path="./", adapter_type="neo4j")`
- [ ] Test initialization with custom connection parameters
- [ ] Test initialization with non-existent repository path
- [ ] Test context manager usage: `with Arc(repo_path="./") as arc:`

### 2.2 Knowledge Graph Building
- [ ] Test basic graph building: `arc build`
- [ ] Test graph building with GitHub integration: `arc build --github`
- [ ] Test graph building with Linear integration: `arc build --linear`
- [ ] Test graph building with LLM enhancement: `arc build --llm-enhancement standard`
- [ ] Test incremental graph building: `arc build --incremental`
- [ ] Test graph building with custom repository path: `arc build --repo /path/to/repo`

### 2.3 Query Functionality
- [ ] Test natural language queries: `arc.query("Why was X implemented?")`
- [ ] Test query with different max_results values
- [ ] Test query with different max_hops values
- [ ] Test query with include_causal=False
- [ ] Test query with cache=False
- [ ] Verify query result structure and fields

### 2.4 Decision Trail Analysis
- [ ] Test getting decision trail for a file line: `arc.get_decision_trail("file.py", 42)`
- [ ] Test with different max_results values
- [ ] Test with different max_hops values
- [ ] Test with include_rationale=False
- [ ] Test with cache=False
- [ ] Verify decision trail result structure and fields

### 2.5 Entity Relationship Exploration
- [ ] Test getting related entities: `arc.get_related_entities("commit:abc123")`
- [ ] Test with specific relationship_types
- [ ] Test with different direction values ("incoming", "outgoing", "both")
- [ ] Test with different max_results values
- [ ] Test with include_properties=True
- [ ] Test with cache=False
- [ ] Verify related entities result structure and fields

### 2.6 Component Impact Analysis
- [ ] Test analyzing component impact: `arc.analyze_component_impact("file:src/auth/login.py")`
- [ ] Test with specific impact_types
- [ ] Test with different max_depth values
- [ ] Test with cache=False
- [ ] Verify impact analysis result structure and fields

### 2.7 Temporal Analysis
- [ ] Test getting entity history: `arc.get_entity_history("file:src/auth/login.py")`
- [ ] Test with specific date ranges
- [ ] Test with include_related=True
- [ ] Test with cache=False
- [ ] Verify history result structure and fields

### 2.8 Graph Export
- [ ] Test exporting graph: `arc.export_graph("abc123", "export.json")`
- [ ] Test with compress=True
- [ ] Test with sign=True
- [ ] Test with different max_hops values
- [ ] Test with enhance_for_llm=False
- [ ] Test with include_causal=False
- [ ] Verify export result structure and file content

## 3. Framework Adapters Testing

### 3.1 LangChain Adapter
- [ ] Test getting LangChain adapter: `get_adapter("langchain")`
- [ ] Test adapting functions: `langchain_adapter.adapt_functions([arc.query, ...])`
- [ ] Test creating LangGraph agent
- [ ] Test creating legacy AgentExecutor
- [ ] Test agent invocation with query
- [ ] Verify agent response structure and content

### 3.2 OpenAI Adapter
- [ ] Test getting OpenAI adapter: `get_adapter("openai")`
- [ ] Test adapting functions: `openai_adapter.adapt_functions([arc.query, ...])`
- [ ] Test creating OpenAI agent
- [ ] Test agent invocation with query
- [ ] Test streaming responses
- [ ] Test creating OpenAI Assistant
- [ ] Verify agent response structure and content

### 3.3 Adapter Registry
- [ ] Test getting all adapters: `get_all_adapters()`
- [ ] Test getting adapter names: `get_adapter_names()`
- [ ] Test discovering adapters: `discover_adapters()`
- [ ] Test registering a custom adapter
- [ ] Test getting a non-existent adapter (error handling)

## 4. CLI Commands Testing

### 4.1 Build Command
- [ ] Test basic build: `arc build`
- [ ] Test build with GitHub: `arc build --github`
- [ ] Test build with Linear: `arc build --linear`
- [ ] Test build with LLM enhancement: `arc build --llm-enhancement standard`
- [ ] Test incremental build: `arc build --incremental`
- [ ] Test build with custom repository path: `arc build --repo /path/to/repo`
- [ ] Test build with custom output path: `arc build --output /path/to/output.db`
- [ ] Test build with max commits limit: `arc build --max-commits 1000`
- [ ] Test build with days limit: `arc build --days 30`

### 4.2 Why Command
- [ ] Test file decision trail: `arc why file src/auth/login.py 42`
- [ ] Test with different max_results values
- [ ] Test with different max_hops values
- [ ] Test with different output formats (text, json, markdown)
- [ ] Test natural language query: `arc why query "Why was X implemented?"`
- [ ] Test with different depth values (shallow, medium, deep)
- [ ] Verify command output structure and content

### 4.3 Export Command
- [ ] Test basic export: `arc export abc123 export.json`
- [ ] Test with compress=True
- [ ] Test with sign=True
- [ ] Test with different max_hops values
- [ ] Test with optimize_for_llm=False
- [ ] Test with include_causal=False
- [ ] Verify export file structure and content

## 5. Documentation Consistency Testing

### 5.1 README.md
- [ ] Verify all examples in README.md work as written
- [ ] Verify installation instructions are correct
- [ ] Verify quick start workflow examples work

### 5.2 Quickstart Guide
- [ ] Verify all steps in quickstart.md work as written
- [ ] Verify time estimates are accurate
- [ ] Test all code examples

### 5.3 API Reference
- [ ] Verify all method signatures in api_reference.md match implementation
- [ ] Verify all parameter descriptions are accurate
- [ ] Verify all return type descriptions are accurate
- [ ] Verify all examples work as written

### 5.4 Framework Adapters Documentation
- [ ] Verify all adapter examples in adapters.md work as written
- [ ] Verify custom adapter creation instructions are correct
- [ ] Test all code examples

## 6. Edge Cases and Error Handling

### 6.1 Error Handling
- [ ] Test with non-existent repository
- [ ] Test with empty repository
- [ ] Test with corrupted database
- [ ] Test with invalid parameters
- [ ] Test with missing dependencies
- [ ] Verify error messages are helpful and actionable

### 6.2 Performance Testing
- [ ] Test with large repository (10,000+ commits)
- [ ] Test with many GitHub issues and PRs
- [ ] Test with complex queries
- [ ] Measure and verify performance metrics

## 7. First-Time User Journey Testing

### 7.1 Complete New Developer Experience
- [ ] Install package and set up authentication
- [ ] Build graph from a small repository
- [ ] Run 3 basic queries about the codebase
- [ ] Integrate with LangChain in under 10 lines of code
- [ ] Measure time taken for each step
- [ ] Verify total time is under 30 minutes

### 7.2 Documentation Navigation
- [ ] Verify links between documentation files work
- [ ] Verify "Next Steps" sections lead to relevant documentation
- [ ] Verify examples are easy to find and follow

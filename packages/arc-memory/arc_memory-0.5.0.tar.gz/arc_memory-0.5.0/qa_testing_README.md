# Arc Memory SDK QA Testing Suite

This directory contains a comprehensive QA testing suite for the Arc Memory SDK. The suite includes scripts to test installation, core functionality, framework adapters, CLI commands, documentation consistency, and the first-time user journey.

## Overview

The QA testing suite is designed to verify that the Arc Memory SDK is ready for open-source release. It focuses on the following areas:

1. **Installation and Setup**: Verifies that the SDK can be installed and set up correctly
2. **Core Functionality**: Tests the core SDK methods like querying, decision trail analysis, and component impact analysis
3. **Framework Adapters**: Tests the LangChain and OpenAI adapters
4. **CLI Commands**: Tests the CLI commands like build, why, and export
5. **Documentation Consistency**: Verifies that the documentation matches the actual API
6. **First-Time User Experience**: Simulates the experience of a first-time user

## Test Scripts

### 1. Installation and Setup Testing

```bash
python qa_test_installation.py
```

This script tests the installation and basic setup of the Arc Memory SDK. It verifies that the package can be imported, the Arc class can be initialized, and basic operations can be performed.

### 2. Core Functionality Testing

```bash
python qa_test_functionality.py
```

This script tests the core functionality of the Arc Memory SDK. It verifies that the SDK can perform basic operations like querying, getting decision trails, and analyzing component impact.

### 3. Framework Adapters Testing

```bash
python qa_test_adapters.py
```

This script tests the framework adapters of the Arc Memory SDK. It verifies that the adapters can be initialized, functions can be adapted, and agents can be created and used.

### 4. CLI Commands Testing

```bash
python qa_test_cli.py
```

This script tests the CLI commands of Arc Memory. It verifies that the commands can be executed and produce the expected output.

### 5. Documentation Consistency Testing

```bash
python qa_test_documentation.py
```

This script tests the consistency of the Arc Memory documentation. It verifies that the examples in the documentation match the actual API, and that the parameter names and descriptions are consistent.

### 6. First-Time User Journey Testing

```bash
python qa_test_user_journey.py
```

This script simulates the experience of a first-time user of Arc Memory. It measures the time taken for each step and verifies that the user can go from zero to working queries in under 30 minutes.

## QA Test Plan

The `qa_test_plan.md` file contains a comprehensive test plan for the Arc Memory SDK. It includes a checklist of tests to perform for each component of the SDK.

## QA Report

The `qa_report.md` file contains a comprehensive report of the QA testing results. It includes findings, issues, and recommendations for improvement.

## Prerequisites

Before running the tests, make sure you have the following:

1. Arc Memory SDK installed with all dependencies:
   ```bash
   pip install arc-memory[all]
   ```

2. Environment variables set up:
   - `GITHUB_TOKEN`: For GitHub integration
   - `LINEAR_API_KEY`: For Linear integration
   - `OPENAI_API_KEY`: For OpenAI integration

   You can set these in a `.env` file in the root directory.

3. A Git repository to test with. The scripts will use the current directory by default.

## Running All Tests

To run all tests in sequence:

```bash
python qa_test_installation.py
python qa_test_functionality.py
python qa_test_adapters.py
python qa_test_cli.py
python qa_test_documentation.py
python qa_test_user_journey.py
```

## Interpreting Results

Each test script will output its results to the console. Look for:

- ✅ Success messages: Indicate that a test passed
- ⚠️ Warning messages: Indicate potential issues that may need attention
- ❌ Error messages: Indicate test failures that need to be addressed

The `qa_report.md` file contains a comprehensive analysis of all test results, including recommendations for improvement.

## Contributing

If you find issues with the Arc Memory SDK or want to improve the QA testing suite, please submit a pull request or open an issue on GitHub.

## License

This QA testing suite is released under the same license as the Arc Memory SDK (MIT).

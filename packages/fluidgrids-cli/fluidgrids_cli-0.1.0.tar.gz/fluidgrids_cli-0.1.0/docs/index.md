# FluidGrids CLI Documentation

Welcome to the FluidGrids CLI documentation! This command-line interface allows you to interact with the FluidGrids Workflow Engine directly from your terminal.

## Table of Contents

- [Installation](installation.md) - How to install the FluidGrids CLI
- [Authentication](authentication.md) - How to authenticate with the FluidGrids API
- [Building Executables](building_executables.md) - How to build standalone executables

## Module Documentation

- [Workflows](workflows.md) - Managing workflow definitions
- [Runs](runs.md) - Triggering and monitoring workflow runs
- [Credentials](credentials.md) - Managing credentials for workflows
- [Configuration](configuration.md) - Managing CLI configuration
- [AI](ai.md) - Using AI to manage workflows
- [Usage](usage.md) - Monitoring workflow engine usage
- [Dashboard](dashboard.md) - Getting insights from the dashboard
- [Search](search.md) - Searching across workflows and runs
- [Nodes](nodes.md) - Managing workflow node types

## Quick Start

```bash
# Install the CLI
pip install fluidgrids-cli

# Authenticate with the API
fluidgrids auth login --url https://api.fluidgrids.ai

# List workflows
fluidgrids workflows list

# Trigger a workflow run
fluidgrids runs trigger my-workflow latest --context '{"input_key": "value"}'

# Get dashboard summary
fluidgrids dashboard summary
```

For more information, see the detailed documentation for each module or run:

```bash
fluidgrids --help
``` 
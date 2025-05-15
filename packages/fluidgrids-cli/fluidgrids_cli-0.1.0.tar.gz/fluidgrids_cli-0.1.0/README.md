# FluidGrids CLI

A command-line interface for the FluidGrids Workflow Engine that allows you to manage workflows, trigger runs, and more.

## Installation

### Using pip

```bash
pip install fluidgrids-cli
```

### From Source

```bash
git clone https://github.com/algoshred/fluidgrids-cli.git
cd fluidgrids-cli
pip install -e .
```

## Quick Start

### Authentication

Set up your credentials first:

```bash
fluidgrids auth login --url https://api.fluidgrids.ai
```

You can also use an API key for automation:

```bash
fluidgrids auth set-key --api-key YOUR_API_KEY
```

### List Workflows

```bash
fluidgrids workflows list
```

### Get Workflow Details

```bash
fluidgrids workflows get KEY VERSION
```

### Trigger a Workflow Run

```bash
fluidgrids runs trigger KEY VERSION --context '{"input_key": "value"}'
```

### Monitor a Run

```bash
fluidgrids runs get RUN_ID
```

## Configuration

The CLI stores configuration in `~/.fluidgrids/config.yaml`. You can view your current configuration with:

```bash
fluidgrids config show
```

## Documentation

For complete documentation, see the [docs directory](docs/) or visit [FluidGrids Documentation](https://docs.fluidgrids.ai/cli).

## License

MIT License - Copyright (c) 2023 Algoshred Technologies Private Limited 
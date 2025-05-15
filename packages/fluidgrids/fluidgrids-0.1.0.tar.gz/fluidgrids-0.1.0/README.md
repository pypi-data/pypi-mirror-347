# FluidGrids SDK

A Python SDK for interacting with the FluidGrids Workflow Engine, by Algoshred Technologies Private Limited.

## Installation

```bash
pip install fluidgrids
```

## Quick Start

```python
from fluidgrids import FluidGridsClient

# Initialize client with your API credentials
client = FluidGridsClient(
    base_url="https://api.fluidgrids.com",
    api_key="your_api_key"
)

# List all workflows
workflows = client.workflows.list()

# Get a specific workflow
workflow = client.workflows.get("workflow-key", "latest")

# Trigger a workflow run
run = client.runs.trigger(
    workflow_key="workflow-key",
    version="latest",
    context={"input_data": "value"}
)

# Check the status of a run
run_status = client.runs.get(run.run_id)
```

## Features

- **Authentication** - Multiple authentication methods (API key, username/password, token)
- **Workflow Management** - Create, update, delete, and manage workflows
- **Run Execution** - Trigger, monitor, and control workflow executions
- **Configuration** - Access and update workflow engine configuration
- **Credentials** - Manage credentials for workflows

## Documentation

For detailed documentation, visit [the FluidGrids SDK documentation](https://docs.fluidgrids.ai/sdk).

## Requirements

- Python 3.8 or higher
- `requests`
- `pydantic`
- `python-dateutil`

## License

MIT

## About

FluidGrids is a workflow engine product by [Algoshred Technologies Private Limited](https://fluidgrids.ai/). The engine allows you to create, manage, and run workflows with ease. 
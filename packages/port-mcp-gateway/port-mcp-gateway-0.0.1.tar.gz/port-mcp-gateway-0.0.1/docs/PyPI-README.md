# Port MCP Gateway

A comprehensive gateway for interacting with Port.io through the PyPort SDK using the Model Context Protocol (MCP).

## Installation

```bash
pip install port-mcp-gateway
```

## Quick Start

1. Set up your Port.io credentials:

```bash
# Create a .env file
echo "PORT_CLIENT_ID=your_client_id" > .env
echo "PORT_CLIENT_SECRET=your_client_secret" >> .env
```

2. Start the gateway:

```bash
port-mcp-gateway
```

3. Access the gateway at http://localhost:8000

## Command Line Options

```
usage: port-mcp-gateway [-h] [--host HOST] [--port PORT] [--reload]
                        [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        [--log-file LOG_FILE] [--env-file ENV_FILE]

Port MCP Gateway

options:
  -h, --help            show this help message and exit
  --host HOST           Host to bind the server to
  --port PORT           Port to bind the server to
  --reload              Enable auto-reload for development
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level
  --log-file LOG_FILE   Log file path
  --env-file ENV_FILE   Environment file path
```

## Using with Cursor or Claude

### For Cursor

```python
import requests
import json

def get_blueprints():
    response = requests.post(
        "http://localhost:8000/mcp/tools/get_blueprints",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"name": "get_blueprints", "input": {}})
    )
    return response.json()

# Use the function
blueprints = get_blueprints()
print(blueprints)
```

### For Claude (via Augment Code Agent)

1. Configure the MCP server in Augment Code Agent:
   - Go to Augment Code Agent settings
   - Navigate to "External Tools" or "Integrations" section
   - Add an MCP Server integration with these details:
     - **Integration Type**: MCP Server
     - **Name**: Port.io Gateway
     - **Command**: `npx -y @augment/mcp-client connect http://localhost:8000/mcp`

2. Use the gateway in conversations with Claude:
   - "Can you use the MCP server to get a list of all my blueprints in Port.io?"
   - "Please use the get_blueprints tool to show me my Port.io blueprints."

## Documentation

For full documentation, visit [GitHub](https://github.com/yourusername/port-mcp-gateway).

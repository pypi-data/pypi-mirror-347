# Port MCP Gateway - Python Package

A Python package for interacting with Port.io through the Machine Conversation Protocol (MCP).

## Installation

```bash
pip install port-mcp-gateway
```

## Usage

```python
from mcp.client.port_client import PortClient
from mcp.models.tool import ToolMap

# Initialize Port client
port_client = PortClient()

# Initialize tool map
tool_map = ToolMap(port_client=port_client)

# Get a tool
blueprint_tool = tool_map.get("get_blueprints")

# Execute the tool
result = blueprint_tool.execute({})
print(result)
```

## Running the MCP Server

```bash
# Run the MCP server
python -m mcp.server

# Or use the console script
port-mcp-gateway
```

## Environment Variables

The following environment variables are required:

- `PORT_CLIENT_ID`: Your Port.io client ID
- `PORT_CLIENT_SECRET`: Your Port.io client secret

## Development

### Prerequisites

- Python 3.8 or higher
- Port.io API credentials

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Port.io API credentials:
   ```bash
   export PORT_CLIENT_ID=your_client_id
   export PORT_CLIENT_SECRET=your_client_secret
   ```

## License

MIT

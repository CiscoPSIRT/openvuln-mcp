# OpenVuln MCP Server

This is a community supported open project of a Model Context Protocol (MCP) server for Cisco Security Advisories. This server provides tools to retrieve and list security advisories from the [Cisco OpenVuln API](https://developer.cisco.com/docs/psirt/). This allows AI application developers to interact with the OpenVuln API using a standardized interface without needing to manage authentication tokens or directly handle the API's complexities.

For detailed documentation, please see the [MCP Server Documentation](./docs/mcp-server-documentation.md).

## Features

- Fetches Cisco security advisories by ID.
- Retrieves CVE details from Cisco.
- Lists the latest Cisco security advisories.
- Filters advisories by severity (Critical, High, Medium, Low).
- Gets advisories related to a specific product name.
- Interacts with the Cisco OpenVuln API integration with Cisco Software Checker. 
- Handles Cisco OpenVuln API authentication seamlessly.

## Getting Started

### Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- Cisco API Client ID and Client Secret. You can obtain these by registering an application on the [Cisco API Console](https://developer.cisco.com/). For more details, see the [authentication guide](https://developer.cisco.com/docs/psirt/authentication/).

### Installation

1.  **Install uv** (if not already installed):
    ```bash
    # On macOS and Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # On Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/CiscoPSIRT/openvuln-mcp.git
    cd openvuln-mcp
    ```

3.  **Install dependencies:**
    ```bash
    uv sync --locked
    ```

### IDE Configuration

This is an stdio-based MCP server that needs to be configured in your IDE's MCP settings. 

1. Locate your IDE's MCP configuration file (commonly `mcp.json` found through IDE's MCP Settings)
2. Add the OpenVuln MCP server configuration:

```json
{
  "mcpServers": {
    "openvuln-mcp": {
      "command": "/path/to/openvuln-mcp/.venv/bin/python3",
      "args": ["/path/to/openvuln-mcp/src/openvuln_mcp_server.py"],
      "env": {
        "CISCO_API_CLIENT_ID": "your_client_id",
        "CISCO_API_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

3. Replace `/path/to/openvuln-mcp` with the actual path to your cloned repository
4. Replace `your_client_id` and `your_client_secret` with your Cisco API credentials
5. Verify the server is connected by checking your IDE's MCP settings - you should see available tools for the openvuln-mcp server

**Note**: On Windows, use `.venv/Scripts/python.exe` instead of `.venv/bin/python3` in the command path.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

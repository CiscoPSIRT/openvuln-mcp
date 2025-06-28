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

- Python 3.x
- Cisco API Client ID and Client Secret. You can obtain these by registering an application on the [Cisco API Console](https://developer.cisco.com/). For more details, see the [authentication guide](https://developer.cisco.com/docs/psirt/authentication/).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CiscoPSIRT/openvuln-mcp.git
    cd openvuln-mcp
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root of the project.
2.  Add your Cisco API credentials to the `.env` file:
    ```
    CISCO_API_CLIENT_ID=your_client_id
    CISCO_API_CLIENT_SECRET=your_client_secret
    ```
    **Note**: For production environments, it is highly recommended to use a secure secret management solution instead of a `.env` file.

### Running the Server

Start the MCP server by running the `openvuln_mcp_server.py` script:

```bash
python src/openvuln_mcp_server.py
```

Once the server is running, it will be accessible to any MCP-compatible client.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

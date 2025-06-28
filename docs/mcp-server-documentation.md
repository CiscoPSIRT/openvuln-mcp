# OpenVuln MCP Server Documentation

This document provides detailed documentation for the OpenVuln Model Context Protocol (MCP) Server, including its architecture, components, and instructions for setup and execution.

## Overview

The OpenVuln MCP Server acts as a bridge between a client application and the [Cisco OpenVuln API.](https://developer.cisco.com/docs/psirt/). It simplifies interaction with the OpenVuln API by handling the OAuth2 authentication and exposing the API's functionality through the MCP protocol. This allows AI application developers to interact with the OpenVuln API using a standardized interface without needing to manage authentication tokens or directly handle the API's intricacies.

## Project Structure

The core logic of the MCP server is contained within the `src` directory, which includes the following key files:

- `openvuln_mcp_server.py`: The main entry point for the server. It initializes and runs the MCP server.
- `auth.py`: Contains the authentication logic, including token management and an authenticated HTTP client.

## `openvuln_mcp_server.py`

This script is responsible for setting up and running the `FastMCP` server.

### Key Components

- **Environment Variables**: The server requires the following environment variables to be set:
  - `CISCO_API_CLIENT_ID`: Your Cisco API client ID.
  - `CISCO_API_CLIENT_SECRET`: Your Cisco API client secret.

Go to the [Cisco PSIRT DevNet site](https://developer.cisco.com/docs/psirt/authentication/) to get more information about how to get your API credentials.

**Note**: While using a `.env` file is convenient for local development, in production environments, you should use more secure methods for managing secrets, such as CyberArk Conjur, AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault. Avoid storing sensitive credentials directly in source-controlled files.


- **TokenManager**: An instance of the `TokenManager` class from `auth.py` is created to manage OAuth2 authentication with the Cisco API.

- **AuthenticatedOpenVulnClient**: An instance of the `AuthenticatedOpenVulnClient` class from `auth.py` is used as the HTTP client. This client automatically injects the necessary authentication token into each request.

- **FastMCP.from_openapi**: The MCP server is created using the `from_openapi` method of the `FastMCP` class. This method takes the OpenVuln OpenAPI specification, the authenticated client, and other configuration parameters to generate the MCP server.

## `auth.py`

This module provides the authentication mechanisms required to interact with the Cisco OpenVuln API.

### `TokenManager` Class

- **Purpose**: The `TokenManager` class is responsible for managing the lifecycle of the OAuth2 token used for authentication. It handles token acquisition, caching, and automatic renewal before expiration.

- **Methods**:
  - `__init__(self, client_id, client_secret, token_url, refresh_margin)`: Initializes the `TokenManager` with the necessary credentials and configuration.
  - `async get_token(self)`: Returns a valid access token, refreshing it if necessary.
  - `async _refresh_token(self)`: Fetches a new access token from the Cisco authentication server.

### `AuthenticatedOpenVulnClient` Class

- **Purpose**: This class is a custom `httpx.AsyncClient` that ensures every request to the OpenVuln API is authenticated. It simplifies the process of making authenticated API calls.

- **Methods**:
  - `__init__(self, token_manager, *args, **kwargs)`: Initializes the client with a `TokenManager` instance.
  - `async send(self, request, *args, **kwargs)`: Intercepts outgoing requests to add the authentication token to the headers. It also includes logic to handle token expiration by refreshing the token and retrying the request if a `403 Forbidden` error is received.

## Setup and Running

To set up and run the OpenVuln MCP Server, follow these steps:

1. **Install Dependencies**: Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**: Create a `.env` file in the root of the project and add your Cisco API credentials:

```
CISCO_API_CLIENT_ID=your_client_id
CISCO_API_CLIENT_SECRET=your_client_secret
```

**Note**: While using a `.env` file is convenient for local development, in production environments, you should use more secure methods for managing secrets, such as CyberArk Conjur, AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault. Avoid storing sensitive credentials directly in source-controlled files.

3. **Run the Server**: Start the MCP server by running the `openvuln_mcp_server.py` script:

```bash
python src/openvuln_mcp_server.py
```

Once the server is running, it will be accessible to any MCP-compatible client, providing a seamless way to interact with the Cisco OpenVuln API.

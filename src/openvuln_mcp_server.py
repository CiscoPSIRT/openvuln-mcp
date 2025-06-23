import httpx
import pyjson5
from fastmcp import FastMCP

# Creating an HTTP client for the Cisco OpenVuln API
client = httpx.AsyncClient(base_url="https://apix.cisco.com/security/advisories/v2/")

# Load the OpenAPI spec for the Cisco OpenVuln API
openapi_spec = pyjson5.loads(httpx.get("https://pubhub.devnetcloud.com/media/psirt/docs/reference/api-v3.json").text)



# Create the MCP server for the Cisco OpenVuln API
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="OpenVuln MCP Server"
)

if __name__ == "__main__":
    mcp.run()
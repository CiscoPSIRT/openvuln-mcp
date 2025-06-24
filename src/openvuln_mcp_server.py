import httpx
import pyjson5
import os
import logging
from fastmcp import FastMCP
from dotenv import load_dotenv
from auth import TokenManager, AuthenticatedOpenVulnClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
CLIENT_ID = os.getenv("CISCO_API_CLIENT_ID")
CLIENT_SECRET = os.getenv("CISCO_API_CLIENT_SECRET")

OPENVULN_BASE_URL = 'https://apix.cisco.com/security/advisories/v2/'
OPENVULN_OAS_URL = 'https://pubhub.devnetcloud.com/media/psirt/docs/reference/api-v3.json' # OpenVuln API OpenAPI spec

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError(
        "Missing required environment variables. "  
        "Please set CISCO_API_CLIENT_ID and CISCO_API_CLIENT_SECRET in .env file."
    )

# Create token manager
token_manager = TokenManager(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
    
# Creating an authenticated HTTP client for the Cisco OpenVuln API
client = AuthenticatedOpenVulnClient(
    token_manager=token_manager,
    base_url=OPENVULN_BASE_URL
)

# Load the OpenAPI spec for the Cisco OpenVuln API
openapi_spec = pyjson5.loads(httpx.get(OPENVULN_OAS_URL).text)

# Create the MCP server for the Cisco OpenVuln API
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="OpenVuln MCP Server",
    dependencies=["pyjson5", "python-dotenv"]
)

if __name__ == "__main__":
    mcp.run()
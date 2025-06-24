import time
import httpx
import asyncio
import logging
from typing import Optional



logger = logging.getLogger(__name__)

class TokenManager:
    """
    Manages OAuth2 token lifecycle for Cisco API authentication.
    Handles token acquisition, and caching.
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str = "https://id.cisco.com/oauth2/default/v1/token",
        refresh_margin: int = 300,  # Refresh token 5 minutes before expiry
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.refresh_margin = refresh_margin
        
        self._token: Optional[str] = None
        self._expiry: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def get_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        async with self._lock:
            if not self._token or not self._expiry or time.time() + self.refresh_margin >= self._expiry:
                await self._refresh_token()
            return self._token
    
    async def _refresh_token(self) -> None:
        """Fetch a new token from the auth server."""
        logger.info("Acquiring new access token")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )
                
                response.raise_for_status()
                token_data = response.json()
                
                self._token = token_data["access_token"]
                # Calculate absolute expiry time
                self._expiry = time.time() + token_data.get("expires_in", 3600)
                
                logger.info(f"Token refreshed successfully. Expires in {token_data.get('expires_in', 3600)} seconds")
                
            except Exception as e:
                logger.error(f"Failed to refresh token: {str(e)}")
                # If we failed and have no token, re-raise the exception
                if not self._token:
                    raise

class AuthenticatedOpenVulnClient(httpx.AsyncClient):
    """Custom HTTP client that automatically adds authentication headers."""
    
    def __init__(self, token_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_manager = token_manager
    
    async def send(self, request, *args, **kwargs):
        # Get current auth token and add to request headers
        auth_token = await self.token_manager.get_token()
        request.headers["Authorization"] = f"Bearer {auth_token}"
        
        # Send the request with the token
        response = await super().send(request, *args, **kwargs)
        
        # Handle 403 by refreshing token and retrying once
        if response.status_code == 403:
            logger.info("Received 403 forbidden, refreshing token and retrying")
            # Force token refresh
            await self.token_manager._refresh_token()
            auth_token = await self.token_manager.get_token()
            request.headers["Authorization"] = f"Bearer {auth_token}"
            response = await super().send(request, *args, **kwargs)
        
        return response

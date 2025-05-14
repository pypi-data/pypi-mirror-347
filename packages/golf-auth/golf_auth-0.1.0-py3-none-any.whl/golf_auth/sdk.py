"""MCP Token Manager SDK for secure OAuth token management."""

import time
import uuid
from typing import Dict, Optional, Any, Callable, Awaitable, List

import httpx
from pydantic import AnyHttpUrl
import base64

# Import shared models
from shared.models import SDKTokenRecord as TokenRecord, SDKSession as Session


class MCPStorageSDK:
    """Client SDK for the MCP Token Storage API.
    
    This SDK abstracts communication with the secure Token Storage API, providing
    a simple interface for storing, retrieving, and refreshing OAuth tokens.
    """
    
    def __init__(
        self, 
        storage_api_endpoint: AnyHttpUrl,
        storage_auth_headers: Dict[str, str],
        provider_name: str,
        supports_refresh: bool = True,
        token_refresh_handler: Optional[Callable[[str], Awaitable[Dict[str, Any]]]] = None,
        default_tenant_id: Optional[uuid.UUID] = None,
        encryption_key: Optional[bytes | str] = None
    ):
        """Initialize the SDK with all necessary configuration.
        
        Args:
            storage_api_endpoint: URL of the token storage API
            storage_auth_headers: Authentication headers for API requests
            provider_name: Name of the OAuth provider (just for labeling)
            supports_refresh: Whether the provider supports refresh tokens
            token_refresh_handler: Async function that takes a refresh_token and returns
                                  new token data. Required if supports_refresh is True.
            default_tenant_id: Optional tenant ID (generated if not provided)
            encryption_key: Encryption key for token encryption (generated if not provided)
                         Can be raw bytes or a base64-encoded string. If string is provided,
                         it will be decoded from base64.
        """
        self.api_url = storage_api_endpoint
        self.auth_headers = storage_auth_headers
        self.client = httpx.AsyncClient(headers=storage_auth_headers)
        self.provider_name = provider_name
        self.supports_refresh = supports_refresh
        self.token_refresh_handler = token_refresh_handler
        self.default_tenant_id = default_tenant_id or uuid.uuid4()
        
        # Validate configuration
        if supports_refresh and token_refresh_handler is None:
            raise ValueError("token_refresh_handler must be provided when supports_refresh is True")
        
        # Set the encryption key
        from shared.crypto import generate_encryption_key
        import logging
        
        if encryption_key:
            # Handle different key formats
            if isinstance(encryption_key, str):
                try:
                    # Try to decode as base64
                    self.encryption_key = base64.b64decode(encryption_key)
                    logging.getLogger(__name__).info("Decoded base64 encryption key")
                except Exception as e:
                    raise ValueError(f"Invalid encryption key format - not valid base64: {e}")
            else:
                # Ensure encryption_key is bytes
                self.encryption_key = encryption_key if isinstance(encryption_key, bytes) else bytes(encryption_key)
        else:
            self.encryption_key = generate_encryption_key()
            logging.getLogger(__name__).warning(
                "No encryption key provided - using temporary key. "
                "Tokens won't persist between restarts."
            )
        
    def _construct_url(self, path: str) -> str:
        """Construct URL with proper path handling.
        
        Args:
            path: The path to append to the base URL
            
        Returns:
            Properly constructed URL without double slashes
        """
        base_url = str(self.api_url).rstrip('/')
        return f"{base_url}/{path.lstrip('/')}"
    
    async def store_provider_token(
        self,
        access_token: str,
        refresh_token: str = "",
        expires_in: int = 3600,
        user_id: Optional[uuid.UUID] = None,
        tenant_id: Optional[uuid.UUID] = None
    ) -> str:
        """Store a provider token securely and return an MCP token.
        
        This handles encryption, storage, and session creation in one call.
        
        Args:
            access_token: Provider access token
            refresh_token: Provider refresh token (empty string if none)
            expires_in: Token expiry in seconds
            user_id: Optional user ID (generated if not provided)
            tenant_id: Optional tenant ID (uses default if not provided)
            
        Returns:
            MCP opaque token for the client
        """
        # Generate UUID if not provided
        if user_id is None:
            user_id = uuid.uuid4()
            
        # Use default tenant if not provided
        if tenant_id is None:
            tenant_id = self.default_tenant_id
            
        # Calculate expiry in milliseconds
        expires_at = int(time.time() * 1000) + (expires_in * 1000)
        
        # Encrypt tokens
        from shared.crypto import encrypt_tokens
        encrypted = encrypt_tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            encryption_key=self.encryption_key
        )
        
        # Store token record
        token_record_id = await self.save_token_record(
            user_id=user_id,
            provider=self.provider_name,
            ciphertext_key=encrypted.ciphertext_key,
            enc_access_token=encrypted.enc_access_token,
            enc_refresh_token=encrypted.enc_refresh_token,
            expires_at=expires_at
        )
        
        # Create session
        mcp_token = await self.create_session(
            token_record_id=token_record_id,
            tenant_id=tenant_id
        )
        
        return mcp_token
    
    async def get_provider_token(
        self,
        mcp_token: str,
        auto_refresh: bool = True
    ) -> str:
        """Get provider token from MCP token with automatic refresh.
        
        This handles session validation, token decryption, and refresh
        if needed - all in one simple call.
        
        Args:
            mcp_token: MCP opaque token from client
            auto_refresh: Whether to refresh if expired
            
        Returns:
            Provider access token ready to use
            
        Raises:
            ValueError: If token is invalid, expired with no refresh capability,
                       or needs reauthorization
        """
        # Validate the session
        session = await self.validate_session(mcp_token)
        if session is None:
            raise ValueError("Invalid or expired session")
        
        # Load the token record
        token_record = await self.load_token_record(session.token_record_id)
        
        # Check if token needs reauthorization
        if token_record.needs_reauth:
            raise ValueError("Token requires reauthorization")
        
        # Decrypt the tokens
        from shared.crypto import decrypt_tokens
        decrypted = decrypt_tokens(
            ciphertext_key=token_record.ciphertext_key,
            enc_access_token=token_record.enc_access_token,
            enc_refresh_token=token_record.enc_refresh_token,
            kek=self.encryption_key,
            expires_at=token_record.expires_at
        )
        
        # For non-refreshable tokens (like GitHub), return the token regardless of expiration
        if not self.supports_refresh:
            return decrypted.access_token
        
        # Check if token needs refresh (only for providers that support refresh)
        current_time = int(time.time() * 1000)
        needs_refresh = decrypted.expires_at <= current_time and decrypted.expires_at > 0
        
        # If token needs refresh, refresh is supported, handler is available, and auto_refresh is enabled
        if needs_refresh and auto_refresh and self.token_refresh_handler and decrypted.refresh_token:
            # Call refresh handler to get new tokens
            try:
                new_tokens = await self.token_refresh_handler(decrypted.refresh_token)
                
                # Encrypt the new tokens
                from shared.crypto import encrypt_tokens
                encrypted = encrypt_tokens(
                    access_token=new_tokens["access_token"],
                    refresh_token=new_tokens.get("refresh_token", decrypted.refresh_token),
                    encryption_key=self.encryption_key
                )
                
                # Update expiry time
                new_expires_at = int(time.time() * 1000) + (new_tokens.get("expires_in", 3600) * 1000)
                
                # Update the token record
                await self.update_token_record(
                    token_record_id=session.token_record_id,
                    enc_access_token=encrypted.enc_access_token,
                    enc_refresh_token=encrypted.enc_refresh_token,
                    ciphertext_key=encrypted.ciphertext_key,
                    expires_at=new_expires_at
                )
                
                return new_tokens["access_token"]
            except Exception as e:
                raise ValueError(f"Failed to refresh token: {str(e)}")
        
        # If token is expired and couldn't be refreshed
        if needs_refresh:
            # For providers with long-lived tokens, expiry is set to 0
            if decrypted.expires_at == 0:
                return decrypted.access_token
                
            # Mark token as needing reauthorization
            await self.update_token_record(
                token_record_id=session.token_record_id,
                needs_reauth=True
            )
            raise ValueError("Token is expired and could not be refreshed")
        
        return decrypted.access_token
    
    async def revoke_provider_token(self, mcp_token: str) -> None:
        """Revoke a provider token by its MCP token.
        
        This only revokes the session, not the underlying token record.
        
        Args:
            mcp_token: MCP opaque token to revoke
            
        Raises:
            ValueError: If token not found
        """
        await self.revoke_session(mcp_token)
    
    async def is_token_valid(self, mcp_token: str) -> bool:
        """Check if an MCP token is valid and not expired.
        
        Args:
            mcp_token: MCP opaque token to check
            
        Returns:
            True if the token is valid and not expired
        """
        try:
            session = await self.validate_session(mcp_token)
            if session is None:
                return False
                
            token_record = await self.load_token_record(session.token_record_id)
            
            if token_record.needs_reauth:
                return False
                
            # Check if expired - for providers without refresh support, consider it valid
            if not self.supports_refresh:
                return True
                
            # For providers with refresh, check expiration
            return token_record.expires_at > int(time.time() * 1000)
        except Exception:
            return False
    
    # The following methods are lower-level API methods for advanced use cases
    
    async def save_token_record(
        self, 
        user_id: uuid.UUID,
        provider: str,
        ciphertext_key: bytes,
        enc_access_token: bytes,
        enc_refresh_token: bytes,
        expires_at: int
    ) -> uuid.UUID:
        """Save a new OAuth token record securely.
        
        Args:
            user_id: User identifier
            provider: OAuth provider name (e.g., "github")
            ciphertext_key: Encrypted key for token decryption
            enc_access_token: Encrypted access token
            enc_refresh_token: Encrypted refresh token
            expires_at: Token expiry time in milliseconds since epoch
            
        Returns:
            UUID of the created token record
        
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url("token-records")
        
        payload = {
            "user_id": str(user_id),
            "provider": provider,
            "ciphertext_key": ciphertext_key.hex(),
            "enc_access_token": enc_access_token.hex(),
            "enc_refresh_token": enc_refresh_token.hex(),
            "expires_at": expires_at
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        return uuid.UUID(data["token_record_id"])
    
    async def load_token_record(self, token_record_id: uuid.UUID) -> TokenRecord:
        """Load a token record by ID.
        
        Args:
            token_record_id: UUID of the token record to load
            
        Returns:
            TokenRecord object containing the encrypted tokens
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"token-records/{token_record_id}")
        
        response = await self.client.get(url)
        response.raise_for_status()
        
        data = response.json()
        return TokenRecord(
            ciphertext_key=bytes.fromhex(data["ciphertext_key"]),
            enc_access_token=bytes.fromhex(data["enc_access_token"]),
            enc_refresh_token=bytes.fromhex(data["enc_refresh_token"]),
            expires_at=data["expires_at"],
            needs_reauth=data["needs_reauth"]
        )
    
    async def update_token_record(
        self,
        token_record_id: uuid.UUID,
        enc_access_token: Optional[bytes] = None,
        enc_refresh_token: Optional[bytes] = None,
        ciphertext_key: Optional[bytes] = None,
        expires_at: Optional[int] = None,
        needs_reauth: Optional[bool] = None
    ) -> None:
        """Update an existing token record.
        
        Args:
            token_record_id: UUID of the token record to update
            enc_access_token: New encrypted access token (optional)
            enc_refresh_token: New encrypted refresh token (optional)
            ciphertext_key: New encrypted key (optional)
            expires_at: New expiry time (optional)
            needs_reauth: Flag indicating if reauthorization is needed (optional)
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"token-records/{token_record_id}")
        
        payload = {}
        if enc_access_token is not None:
            payload["enc_access_token"] = enc_access_token.hex()
        if enc_refresh_token is not None:
            payload["enc_refresh_token"] = enc_refresh_token.hex()
        if ciphertext_key is not None:
            payload["ciphertext_key"] = ciphertext_key.hex()
        if expires_at is not None:
            payload["expires_at"] = expires_at
        if needs_reauth is not None:
            payload["needs_reauth"] = needs_reauth
        
        response = await self.client.patch(url, json=payload)
        response.raise_for_status()
    
    async def create_session(
        self,
        token_record_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> str:
        """Create an MCP session (opaque token) linked to a token record.
        
        Args:
            token_record_id: UUID of the token record
            tenant_id: UUID of the tenant
            
        Returns:
            Opaque MCP token string
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url("sessions")
        
        payload = {
            "token_record_id": str(token_record_id),
            "tenant_id": str(tenant_id)
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        return data["mcp_token"]
    
    async def validate_session(self, mcp_token: str) -> Optional[Session]:
        """Validate an MCP session token.
        
        Args:
            mcp_token: MCP opaque token string
            
        Returns:
            Session object if valid, None if invalid
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"sessions/{mcp_token}")
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            data = response.json()
            return Session(
                token_record_id=uuid.UUID(data["token_record_id"]),
                tenant_id=uuid.UUID(data["tenant_id"])
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    async def revoke_session(self, mcp_token: str) -> None:
        """Revoke an MCP session token.
        
        Args:
            mcp_token: MCP opaque token string
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"sessions/{mcp_token}")
        
        response = await self.client.delete(url)
        response.raise_for_status()
    
    async def __aenter__(self):
        """Context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with client cleanup."""
        await self.client.aclose()
    
    def close(self):
        """Close the HTTP client."""
        self.client.aclose()

    # OAuth client management methods
    
    async def save_oauth_client(
        self,
        client_id: str,
        client_secret: str = "",
        redirect_uris: List[str] = None,
        scopes: List[str] = None
    ) -> str:
        """Save an OAuth client to the persistent storage.
        
        Args:
            client_id: Unique client identifier
            client_secret: Optional client secret
            redirect_uris: List of allowed redirect URIs
            scopes: List of allowed scopes
            
        Returns:
            Client ID of the saved client
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url("oauth-clients")
        
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris or [],
            "scopes": scopes or []
        }
        
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        
        return client_id
    
    async def get_oauth_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get an OAuth client from persistent storage.
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Client data or None if not found
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"oauth-clients/{client_id}")
        
        try:
            response = await self.client.get(url)
            if response.status_code == 404:
                return None
                
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    async def list_oauth_clients(self) -> List[Dict[str, Any]]:
        """List all OAuth clients from persistent storage.
        
        Returns:
            List of client data dictionaries
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url("oauth-clients")
        
        response = await self.client.get(url)
        response.raise_for_status()
        
        return response.json()
    
    async def delete_oauth_client(self, client_id: str) -> None:
        """Delete an OAuth client from persistent storage.
        
        Args:
            client_id: Unique client identifier
            
        Raises:
            httpx.HTTPError: If the API request fails
        """
        url = self._construct_url(f"oauth-clients/{client_id}")
        
        response = await self.client.delete(url)
        response.raise_for_status() 
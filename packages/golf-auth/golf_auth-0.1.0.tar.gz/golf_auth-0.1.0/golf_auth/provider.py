"""Provider interface for MCP Token Manager.

This module defines the OAuthProviderInterface abstract base class that OAuth providers
should implement to work with the MCP Token Manager.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Any
import uuid


class OAuthProviderInterface(ABC):
    """Abstract base class for OAuth providers to implement.
    
    This interface defines the methods that an OAuth provider needs to implement
    to work with the MCP Token Manager. Implementing this interface allows the
    Token Manager to handle token storage and retrieval in a consistent way
    across different OAuth providers.
    """
    
    @abstractmethod
    async def store_token(
        self,
        access_token: str,
        refresh_token: str,
        expires_in: int,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID
    ) -> str:
        """Store an OAuth token securely and return an MCP token.
        
        Args:
            access_token: Provider access token
            refresh_token: Provider refresh token (empty if none)
            expires_in: Token expiry in seconds
            user_id: User identifier
            tenant_id: Tenant identifier
            
        Returns:
            MCP opaque token for client use
        """
        pass
    
    @abstractmethod
    async def get_token(self, mcp_token: str) -> str:
        """Get the provider token for the given MCP token.
        
        Args:
            mcp_token: MCP opaque token
            
        Returns:
            Provider access token ready to use
            
        Raises:
            ValueError: If token is invalid or expired
        """
        pass
    
    @abstractmethod
    async def is_token_valid(self, mcp_token: str) -> bool:
        """Check if an MCP token is valid.
        
        Args:
            mcp_token: MCP opaque token
            
        Returns:
            True if token is valid, False otherwise
        """
        pass
    
    @abstractmethod
    async def revoke_token(self, mcp_token: str) -> None:
        """Revoke an MCP token.
        
        Args:
            mcp_token: MCP opaque token to revoke
            
        Raises:
            ValueError: If token not found
        """
        pass
    
    @abstractmethod
    async def save_client(
        self,
        client_id: str,
        client_secret: str = "",
        redirect_uris: List[str] = None,
        scopes: List[str] = None
    ) -> str:
        """Save an OAuth client.
        
        Args:
            client_id: Unique client identifier
            client_secret: Client secret
            redirect_uris: List of allowed redirect URIs
            scopes: List of allowed scopes
            
        Returns:
            Client ID of the saved client
        """
        pass
    
    @abstractmethod
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get an OAuth client by ID.
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Client data or None if not found
        """
        pass
    
    @abstractmethod
    async def list_clients(self) -> List[Dict[str, Any]]:
        """List all OAuth clients.
        
        Returns:
            List of client data dictionaries
        """
        pass
    
    @abstractmethod
    async def delete_client(self, client_id: str) -> None:
        """Delete an OAuth client.
        
        Args:
            client_id: Unique client identifier
        """
        pass

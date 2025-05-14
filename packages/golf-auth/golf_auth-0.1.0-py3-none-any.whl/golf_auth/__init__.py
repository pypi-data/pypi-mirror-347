"""Golf Auth - Secure OAuth token storage and management for MCP servers."""

__version__ = "0.1.0"

# Import main components for easy access
from .sdk import MCPStorageSDK
from shared.models import SDKTokenRecord as TokenRecord, SDKSession as Session
from shared.crypto import encrypt_tokens, decrypt_tokens, generate_encryption_key
from .provider import OAuthProviderInterface

__all__ = [
    "MCPStorageSDK",
    "TokenRecord",
    "Session",
    "encrypt_tokens",
    "decrypt_tokens",
    "generate_encryption_key",
    "OAuthProviderInterface",
] 
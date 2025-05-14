# MCP Auth System

A secure token storage and authentication system for OAuth integrations in the MCP (Model Context Protocol) server.

## Overview

The MCP Auth System provides a secure OAuth token storage solution with a two-tier approach:

1. **Token Records**: Encrypted OAuth credentials (access tokens, refresh tokens)
2. **Sessions**: Opaque MCP tokens mapped to token records

A key feature is that when clients disconnect, only their session is revoked—not the underlying token record. This allows for reconnection without re-authorization if the client has saved their MCP token. This implementation supports various OAuth providers while maintaining strong security through envelope encryption.

## Architecture

### Components

1. **Token Storage Service**: Backend service that securely stores and manages OAuth tokens
2. **MCP Storage SDK**: Client library for interacting with the token storage service
3. **Integration Layer**: Provider-specific implementations (e.g., GitHub OAuth integration)
4. **Cryptographic Utilities**: Provides tools for secure token encryption/decryption

### Data Model

The system uses three primary entities:

1. **Token Records**: Stores encrypted provider tokens with the following attributes:
   - `token_record_id`: Unique identifier (UUID)
   - `user_id`: User identifier (UUID)
   - `provider`: OAuth provider name (string)
   - `ciphertext_key`: Encrypted data encryption key (bytes)
   - `enc_access_token`: Encrypted access token (bytes)
   - `enc_refresh_token`: Encrypted refresh token (bytes)
   - `expires_at`: Token expiry timestamp (milliseconds since epoch)
   - `needs_reauth`: Flag indicating if re-authorization is required (boolean)

2. **Sessions**: Links users to token records with the following attributes:
   - `session_id`: Unique identifier (UUID)
   - `mcp_token`: Opaque token for client use (string)
   - `token_record_id`: Reference to token record (UUID)
   - `tenant_id`: Multi-tenant identifier (UUID)
   - `created_at`: Creation timestamp
   - `expires_at`: Session expiry timestamp

3. **OAuth Clients**: Stores registered OAuth clients:
   - `client_id`: Unique client identifier (string)
   - `client_secret`: Client secret (string)
   - `redirect_uris`: List of allowed redirect URIs (array)
   - `scopes`: List of allowed scopes (array)

## Security Implementation

### Envelope Encryption

The system uses envelope encryption (KEK/DEK pattern) to protect OAuth tokens:

1. **Master Encryption Key (KEK)**: A key encryption key provided at startup
2. **Data Encryption Key (DEK)**: Generated per token record to encrypt tokens
3. **Process**:
   - Generate a random DEK for each token record
   - Encrypt access and refresh tokens with the DEK
   - Encrypt the DEK with the KEK
   - Store the encrypted DEK (ciphertext_key), encrypted tokens, but never the raw DEK

```
┌─────────────┐     Encrypts     ┌─────────────┐     Encrypts     ┌─────────────┐
│     KEK     ├─────────────────>│     DEK     ├─────────────────>│   Tokens    │
│ (Master Key)│                  │ (Data Key)  │                  │             │
└─────────────┘                  └─────────────┘                  └─────────────┘
      │                                 │                               │
      │                                 │                               │
      │                                 ▼                               ▼
      │                          ┌─────────────┐               ┌─────────────┐
      │                          │ Encrypted   │               │ Encrypted   │
      │                          │     DEK     │               │   Tokens    │
      │                          └─────────────┘               └─────────────┘
      │                                 │                               │
      ▼                                 │                               │
┌─────────────┐                         │                               │
│  Persisted  │                         │                               │
│  in Server  │                         ▼                               ▼
│ Environment │                  ┌─────────────────────────────────────────┐
└─────────────┘                  │              Database                   │
                                 └─────────────────────────────────────────┘
```

### Key Management

- The KEK must be provided securely to the application and remain consistent across restarts
- It can be supplied as a base64-encoded string via environment variables
- Use a secure key management system (like AWS KMS or HashiCorp Vault) in production

## Getting Started

### Prerequisites

- Python 3.8+
- Dependencies listed in requirements.txt

### Installation

```bash
pip install -r requirements.txt
```

## MCP Storage SDK Usage

The SDK provides a simple interface for interacting with the token storage:

### Core Functions

- `store_provider_token()`: Encrypts and stores provider tokens, returning an MCP token
- `get_provider_token()`: Retrieves and decrypts provider tokens using an MCP token
- `revoke_provider_token()`: Invalidates sessions
- `is_token_valid()`: Verifies token validity

### Client Management

- `save_oauth_client()`: Stores OAuth client configuration
- `get_oauth_client()`: Retrieves client configuration
- `list_oauth_clients()`: Lists all registered clients
- `delete_oauth_client()`: Removes client configuration

### Initialization

```python
from pydantic import AnyHttpUrl
from golf_auth import MCPStorageSDK

storage_sdk = MCPStorageSDK(
    storage_api_endpoint=AnyHttpUrl("http://localhost:8010"),
    storage_auth_headers={"X-API-Key": "api-token-here"},
    provider_name="github",
    supports_refresh=False,  # Provider-specific setting
    encryption_key="base64-encoded-key-here"
)
```

### Complete Example

```python
import uuid
from pydantic import AnyHttpUrl
from golf_auth import MCPStorageSDK

# Initialize the SDK
storage_sdk = MCPStorageSDK(
    storage_api_endpoint=AnyHttpUrl("https://your-storage-api.internal"),
    storage_auth_headers={"X-API-Key": "your-service-auth-token"},
    provider_name="github",
    supports_refresh=False,  # GitHub tokens don't expire
    encryption_key="base64-encoded-key-here"
)

# Store a provider token securely
async def save_oauth_tokens(access_token, refresh_token, expires_in, user_id, tenant_id):
    # Store tokens and get an MCP token back
    mcp_token = await storage_sdk.store_provider_token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        user_id=user_id,
        tenant_id=tenant_id
    )
    
    return mcp_token

# Get a provider token with automatic refresh
async def get_provider_token(mcp_token):
    # Get the provider token (with automatic refresh if needed)
    return await storage_sdk.get_provider_token(mcp_token)

# Check if a token is valid
async def is_token_valid(mcp_token):
    return await storage_sdk.is_token_valid(mcp_token)

# Revoke a token (for logout)
async def logout(mcp_token):
    await storage_sdk.revoke_provider_token(mcp_token)
```

## Provider Integration

### Example: GitHub OAuth Provider

The GitHub integration demonstrates how to extend the system with provider-specific behavior:

1. **Authorization Flow**:
   - The provider generates an authorization URL for GitHub
   - Handles the callback, exchanging the code for a GitHub token
   - Stores the token securely via the SDK
   - Issues an MCP token to the client

2. **Token Acquisition**:
   - When a client needs to use the GitHub API, the MCP token is exchanged for the actual GitHub token
   - This happens transparently, with automatic refresh if supported by the provider

### Non-refreshable Token Handling

Some providers (like GitHub) issue long-lived tokens without refresh capabilities:

- Set `supports_refresh=False` during SDK initialization
- Use `expires_in=0` to indicate a non-expiring token
- The system will handle these appropriately, skipping refresh attempts

### OAuth Client Persistence

Clients are stored in the database rather than memory:

```python
async def get_client(self, client_id: str) -> Optional[OAuthClientInformationFull]:
    """Get OAuth client information from persistent storage."""
    client_data = await self.storage_sdk.get_oauth_client(client_id)
    if client_data:
        return OAuthClientInformationFull(
            client_id=client_data["client_id"],
            client_secret=client_data["client_secret"],
            redirect_uris=client_data["redirect_uris"],
            scopes=client_data["scopes"]
        )
    return None
```

## Migration Guide: From In-Memory to Secure Token Storage

This section provides a detailed guide for migrating from an in-memory OAuth implementation to the secure token storage system.

### Comparison: In-Memory vs. Secure Storage

| Feature | In-Memory (server.py) | Secure Storage (integrated_server.py) |
|---------|----------------------|--------------------------------------|
| Token Storage | In-memory dictionaries | Encrypted in database with two-tier approach |
| Persistence | Lost on server restart | Persists through restarts |
| Security | Plain text tokens in memory | Envelope encryption (KEK/DEK) |
| Client Storage | In-memory dictionary | Database with persistence |
| Token Refresh | Basic or unsupported | Automatic with configurable handlers |
| Multi-instance Support | Not supported | Fully supported (shared database) |

### Step-by-Step Migration Process

1. **Add Dependencies**

   First, ensure your project has access to the MCP Auth SDK:

   ```python
   # Add the project root to your path if the SDK is in a parent directory
   import sys
   import os
   project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
   sys.path.insert(0, project_root)
   
   # Import the SDK
   from golf_auth import MCPStorageSDK
   ```

2. **Update Settings**

   Add the necessary configuration settings:

   ```python
   class ServerSettings(BaseSettings):
       # Existing settings...
       
       # Add Token Storage settings
       token_storage_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8010")
       token_storage_auth_token: str = "dev-api-key"  
       encryption_key: str = ""  # Base64 encoded key
   ```

3. **Initialize the SDK**

   Create and configure the storage SDK:

   ```python
   # Initialize the MCPStorageSDK
   storage_sdk = MCPStorageSDK(
       storage_api_endpoint=AnyHttpUrl(api_url),
       storage_auth_headers={"X-API-Key": settings.token_storage_auth_token},
       provider_name="github",
       supports_refresh=False,  # Provider specific
       encryption_key=settings.encryption_key
   )
   ```

4. **Modify the OAuth Provider**

   Replace in-memory storage with SDK calls:

   Before (In-Memory):
   ```python
   # Generate MCP access token
   mcp_token = f"mcp_{secrets.token_hex(32)}"

   # Store MCP token in memory
   self.tokens[mcp_token] = AccessToken(
       token=mcp_token,
       client_id=client.client_id,
       scopes=authorization_code.scopes,
       expires_at=int(time.time()) + 3600,
   )

   # Store mapping between MCP token and GitHub token
   if github_token:
       self.token_mapping[mcp_token] = github_token
   ```

   After (Secure Storage):
   ```python
   # Store in secure storage
   user_id = uuid.uuid4()  # In a real app from context
   tenant_id = uuid.UUID(client.client_id)
   
   # Store token and get back MCP token
   mcp_token = await self.storage_sdk.store_provider_token(
       access_token=github_token,
       refresh_token="",  # GitHub doesn't provide refresh tokens
       expires_in=0,  # GitHub tokens don't expire
       user_id=user_id,
       tenant_id=tenant_id
   )
   ```

5. **Update Token Validation**

   Before (In-Memory):
   ```python
   async def load_access_token(self, token: str) -> AccessToken | None:
       """Load and validate an access token."""
       access_token = self.tokens.get(token)
       if not access_token:
           return None

       # Check if expired
       if access_token.expires_at and access_token.expires_at < time.time():
           del self.tokens[token]
           return None

       return access_token
   ```

   After (Secure Storage):
   ```python
   async def load_access_token(self, token: str) -> Optional[AccessToken]:
       """Load and validate an access token."""
       try:
           is_valid = await self.storage_sdk.is_token_valid(token)
           if is_valid:
               return AccessToken(
                   token=token,
                   client_id="",  # We don't track this in storage
                   scopes=[self.settings.mcp_scope],
                   expires_at=None,  # GitHub tokens don't expire
               )
       except Exception as e:
           logger.warning(f"Error checking token in storage: {e}")
       
       return None
   ```

6. **Update Token Retrieval**

   Before (In-Memory):
   ```python
   def get_github_token() -> str:
       """Get the GitHub token for the authenticated user."""
       access_token = get_access_token()
       if not access_token:
           raise ValueError("Not authenticated")

       # Get GitHub token from mapping
       github_token = oauth_provider.token_mapping.get(access_token.token)

       if not github_token:
           raise ValueError("No GitHub token found for user")

       return github_token
   ```

   After (Secure Storage):
   ```python
   async def get_github_token() -> str:
       """Get the GitHub token for the authenticated user."""
       access_token = get_access_token()
       if not access_token:
           raise ValueError("Not authenticated")

       try:
           # Get token from secure storage
           return await oauth_provider.get_provider_token(access_token.token)
       except Exception as e:
           raise ValueError(f"No GitHub token found: {e}")
   ```

7. **Update Client Management**

   Before (In-Memory):
   ```python
   async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
       """Get OAuth client information."""
       return self.clients.get(client_id)

   async def register_client(self, client_info: OAuthClientInformationFull):
       """Register a new OAuth client."""
       self.clients[client_info.client_id] = client_info
   ```

   After (Secure Storage):
   ```python
   async def get_client(self, client_id: str) -> Optional[OAuthClientInformationFull]:
       """Get OAuth client information from persistent storage."""
       client_data = await self.storage_sdk.get_oauth_client(client_id)
       if client_data:
           return OAuthClientInformationFull(
               client_id=client_data["client_id"],
               client_secret=client_data["client_secret"],
               redirect_uris=client_data["redirect_uris"],
               scopes=client_data["scopes"]
           )
       return None

   async def register_client(self, client_info: OAuthClientInformationFull):
       """Register a new OAuth client in persistent storage."""
       # Convert space-separated scope string to a list of scopes
       scopes = client_info.scope.split() if client_info.scope else []
       await self.storage_sdk.save_oauth_client(
           client_id=client_info.client_id,
           client_secret=client_info.client_secret,
           redirect_uris=[str(uri) for uri in client_info.redirect_uris],
           scopes=scopes
       )
   ```

8. **Add Token Revocation**

   ```python
   async def revoke_token(self, token: str, token_type_hint: Optional[str] = None) -> None:
       """Revoke a token."""
       try:
           await self.storage_sdk.revoke_provider_token(token)
       except Exception as e:
           logger.warning(f"Error revoking token in storage: {e}")
           raise ValueError(f"Failed to revoke token: {e}")
   ```

9. **Add Error Handling**

   Ensure proper error handling throughout:
   
   ```python
   try:
       # Operation using SDK
       result = await storage_sdk.some_operation()
   except Exception as e:
       logger.error(f"Storage operation failed: {e}")
       # Appropriate error response
       raise ValueError(f"Operation failed: {e}")
   ```

10. **Add Validation for Required Settings**

    ```python
    if not settings.token_storage_url:
        logger.error("Token storage URL is required")
        logger.error("Set MCP_GITHUB_TOKEN_STORAGE_URL environment variable")
        return 1
    
    if not settings.token_storage_auth_token:
        logger.error("Token storage auth token is required")
        logger.error("Set MCP_GITHUB_TOKEN_STORAGE_AUTH_TOKEN environment variable")
        return 1
        
    logger.info(f"Using token storage service at {settings.token_storage_url}")
    ```

### Complete Example

The complete example can be found in the file `examples/servers/simple-auth/mcp_simple_auth/integrated_server.py`. This implementation demonstrates a GitHub OAuth provider that uses the secure token storage system.

Key features demonstrated:

1. **Stateless Operation**: The server can restart without losing tokens
2. **Enhanced Security**: Tokens are encrypted and never stored in plaintext
3. **Proper Key Management**: KEK is configured at startup and persisted
4. **Client Persistence**: OAuth clients survive server restarts
5. **Error Handling**: Comprehensive error handling for all operations
6. **Provider-Specific Logic**: Support for GitHub's non-refreshable tokens

## Error Handling

The system implements comprehensive error handling for token operations:

1. **Token Validation Failures**
   - Invalid tokens return `None` or raise appropriate errors
   - Expired tokens are either refreshed automatically or marked for re-authorization

2. **Refresh Failures**
   - Tokens that fail to refresh are marked with `needs_reauth=True`
   - Clients must re-authenticate when encountering this state

3. **Encryption Errors**
   - Encryption/decryption failures generate clear error messages
   - The system fails securely, never exposing sensitive token data

## Best Practices

1. **Key Management**
   - Use a dedicated key management service for the KEK in production
   - Rotate keys periodically according to your security policy
   - Never store the KEK in plain text in configuration files

2. **Token Lifecycle**
   - Implement token revocation when users log out
   - Consider session timeouts for sensitive applications
   - Periodically clean up expired sessions

3. **Security Considerations**
   - Ensure the token storage service is properly secured with authentication
   - Use HTTPS for all communication between components
   - Monitor for suspicious activity such as excessive token refreshes

## Integration with MCP Server

The MCP Storage SDK is designed to be integrated with your MCP Server implementation to provide secure OAuth token storage. The typical integration flow is:

1. **OAuth authorization flow**: Your MCP Server handles the OAuth authorization flow with providers
2. **Token storage**: The SDK stores the resulting tokens securely
3. **Token retrieval**: The SDK retrieves and automatically refreshes tokens when needed
4. **Session management**: The SDK manages opaque session tokens

Here's a complete integration example connecting an MCP server with GitHub OAuth:

```python
# Initialize the MCPStorageSDK
storage_sdk = MCPStorageSDK(
    storage_api_endpoint=AnyHttpUrl(api_url),
    storage_auth_headers={"X-API-Key": settings.token_storage_auth_token},
    provider_name="github",
    supports_refresh=False,  # GitHub tokens don't expire
    encryption_key=settings.encryption_key
)

# Create the GitHub OAuth provider with storage integration
oauth_provider = SimpleGitHubOAuthProviderWithStorage(settings, storage_sdk)

# Create the MCP server with the provider
app = FastMCP(
    name="GitHub MCP Server with Token Storage",
    instructions="MCP server with GitHub OAuth and secure token storage",
    auth_server_provider=oauth_provider,
    host=settings.host,
    port=settings.port,
    debug=True,
    auth=auth_settings,
)
```

## Extending the System

To add support for a new OAuth provider:

1. Create a provider-specific implementation of `OAuthAuthorizationServerProvider`
2. Configure the SDK with appropriate provider settings
3. Implement the necessary authorization, token exchange, and refresh logic
4. Update the UI to expose the new provider option to users

## Troubleshooting

Common issues and solutions:

1. **422 Unprocessable Entity when registering clients**
   - Ensure scope format is correct (list of strings, not space-separated string)
   - Verify client_id format is valid

2. **Token decryption failures**
   - Check that the KEK is consistent across restarts
   - Verify the token record exists and has valid encrypted data

3. **Session validation failures**
   - Confirm the session hasn't expired
   - Check that the referenced token record still exists

## Conclusion

The MCP Auth System provides a secure, flexible foundation for OAuth token management with strong encryption, proper session handling, and provider-specific customization. This implementation separates token storage from application logic, allowing for better security practices and scalability.

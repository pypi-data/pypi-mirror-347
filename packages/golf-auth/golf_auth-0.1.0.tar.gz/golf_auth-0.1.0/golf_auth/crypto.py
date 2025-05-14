"""Cryptographic utilities for OAuth token encryption and decryption."""

import os
import logging


from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel


class TokenEncryption(BaseModel):
    """Model for encrypted token data."""
    enc_access_token: bytes
    enc_refresh_token: bytes
    ciphertext_key: bytes


class TokenDecryption(BaseModel):
    """Model for decrypted token data."""
    access_token: str
    refresh_token: str
    expires_at: int


def generate_encryption_key() -> bytes:
    """Generate a new random encryption key.
    
    Returns:
        Random 32-byte key suitable for AES-GCM
    """
    return AESGCM.generate_key(bit_length=256)


def encrypt_tokens(
    access_token: str,
    refresh_token: str,
    encryption_key: bytes = None
) -> TokenEncryption:
    """Encrypt OAuth tokens using AES-GCM with a persistent key.
    
    Args:
        access_token: Raw access token string
        refresh_token: Raw refresh token string
        encryption_key: Encryption key (required) - this is the master KEK
        
    Returns:
        TokenEncryption object containing encrypted tokens and key
    """
    # Generate a new data encryption key (DEK)
    dek = generate_encryption_key()
    
    # Create DEK cipher for token encryption
    dek_cipher = AESGCM(dek)
    
    # Generate unique nonces for each token
    access_nonce = os.urandom(12)
    refresh_nonce = os.urandom(12)
    
    # Encrypt the tokens using DEK
    enc_access_token = access_nonce + dek_cipher.encrypt(
        access_nonce,
        access_token.encode('utf-8'),
        None
    )
    
    enc_refresh_token = refresh_nonce + dek_cipher.encrypt(
        refresh_nonce,
        refresh_token.encode('utf-8'),
        None
    )
    
    # Use the provided master KEK to encrypt the DEK
    kek_cipher = AESGCM(encryption_key)
    
    # Encrypt the DEK with the master KEK
    key_nonce = os.urandom(12)
    ciphertext_key = key_nonce + kek_cipher.encrypt(
        key_nonce,
        dek,
        None
    )
    
    return TokenEncryption(
        enc_access_token=enc_access_token,
        enc_refresh_token=enc_refresh_token,
        ciphertext_key=ciphertext_key
    )


def decrypt_tokens(
    ciphertext_key: bytes,
    enc_access_token: bytes,
    enc_refresh_token: bytes,
    kek: bytes,
    expires_at: int = 0
) -> TokenDecryption:
    """Decrypt tokens using envelope encryption.
    
    Args:
        ciphertext_key: Ciphertext of data encryption key
        enc_access_token: Ciphertext access token
        enc_refresh_token: Ciphertext refresh token
        kek: Key encryption key (KEK) - must be the same key used during encryption
        expires_at: Token expiry time
        
    Returns:
        TokenDecryption with decrypted tokens
    """
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Attempting to decrypt tokens with key length: {len(kek)}")
        logger.info(f"Key bytes (first 8): {kek[:8].hex()}")
        logger.info(f"Ciphertext key bytes (first 16): {ciphertext_key[:16].hex()}")
        
        # Decrypt the data encryption key
        try:
            cipher = AESGCM(kek)
            
            # The first 12 bytes of ciphertext are the nonce
            nonce = ciphertext_key[:12]
            ciphertext = ciphertext_key[12:]
            
            logger.info(f"Nonce length: {len(nonce)}, Ciphertext length: {len(ciphertext)}")
            dek = cipher.decrypt(nonce, ciphertext, None)
            logger.info(f"Successfully decrypted DEK, length: {len(dek)}")
        except Exception as e:
            logger.error(f"Error decrypting data encryption key: {type(e).__name__}: {e}")
            raise ValueError(f"Failed to decrypt key: {e}")
        
        # Decrypt access token
        try:
            data_cipher = AESGCM(dek)
            access_nonce = enc_access_token[:12]
            access_ciphertext = enc_access_token[12:]
            access_token = data_cipher.decrypt(access_nonce, access_ciphertext, None)
            logger.info("Successfully decrypted access token")
        except Exception as e:
            logger.error(f"Error decrypting access token: {e}")
            raise ValueError(f"Failed to decrypt access token: {e}")
            
        # Decrypt refresh token
        try:
            refresh_nonce = enc_refresh_token[:12]
            refresh_ciphertext = enc_refresh_token[12:]
            refresh_token = data_cipher.decrypt(refresh_nonce, refresh_ciphertext, None)
            logger.info("Successfully decrypted refresh token")
        except Exception as e:
            logger.error(f"Error decrypting refresh token: {e}")
            raise ValueError(f"Failed to decrypt refresh token: {e}")
        
        return TokenDecryption(
            access_token=access_token.decode('utf-8'),
            refresh_token=refresh_token.decode('utf-8'),
            expires_at=expires_at
        )
    except ValueError as e:
        # Re-raise ValueError with the original message
        raise e
    except Exception as e:
        logger.exception("Unexpected error during token decryption")
        raise ValueError(f"Failed to decrypt tokens: {type(e).__name__}: {e}") 
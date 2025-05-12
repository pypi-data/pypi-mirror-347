"""
Encryption Service Module for Secure Model Service

This module provides encryption and decryption capabilities for model weights,
implementing both AES and Kyber post-quantum encryption methods.
"""

import os
import json
import logging
from typing import Dict, Any, Tuple, Optional, Union

import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pqcrypto.kem.kyber as kyber

logger = logging.getLogger(__name__)


class EncryptionService:
    """Service for encrypting and decrypting model weights using AES and Kyber algorithms."""

    def __init__(self, kms_key_arn: Optional[str] = None, client_id: str = "default"):
        """
        Initialize the encryption service.

        Args:
            kms_key_arn: ARN of the KMS key for encryption (if using AWS KMS)
            client_id: Unique identifier for the client
        """
        self.client_id = client_id
        self.kms_key_arn = kms_key_arn
        self._kms_client = None if not kms_key_arn else boto3.client("kms")

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """
        Derive an encryption key from password and salt using PBKDF2.

        Args:
            password: Password for key derivation
            salt: Salt for key derivation

        Returns:
            Derived key as bytes
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(password.encode())

    def generate_kyber_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a Kyber post-quantum key pair.

        Returns:
            Tuple of (public_key, private_key) as bytes
        """
        public_key, private_key = kyber.Kyber1024.keygen()
        return public_key, private_key

    def encrypt_with_aes(self, data: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt data using AES-GCM.

        Args:
            data: Data to encrypt
            key: AES encryption key

        Returns:
            Tuple of (nonce, ciphertext) as bytes
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # 96-bit nonce
        ciphertext = aesgcm.encrypt(nonce, data, None)
        return nonce, ciphertext

    def decrypt_with_aes(self, nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
        """
        Decrypt data using AES-GCM.

        Args:
            nonce: Nonce used during encryption
            ciphertext: Encrypted data
            key: AES encryption key

        Returns:
            Decrypted data as bytes
        """
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    def encrypt_with_kyber(self, data: bytes, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt data using Kyber KEM.

        Args:
            data: Data to encrypt
            public_key: Kyber public key

        Returns:
            Tuple of (ciphertext, shared_secret) as bytes
        """
        ciphertext, shared_secret = kyber.Kyber1024.enc(public_key)
        # Use the shared secret to encrypt the data with AES
        nonce, encrypted_data = self.encrypt_with_aes(data, shared_secret)
        # Return the Kyber ciphertext and the AES-encrypted data
        return ciphertext, nonce + encrypted_data

    def decrypt_with_kyber(self, ciphertext: bytes, private_key: bytes, aes_data: bytes) -> bytes:
        """
        Decrypt data that was encrypted using Kyber KEM.

        Args:
            ciphertext: Kyber ciphertext
            private_key: Kyber private key
            aes_data: AES-encrypted data with nonce prepended

        Returns:
            Decrypted data as bytes
        """
        # Extract the shared secret using Kyber
        shared_secret = kyber.Kyber1024.dec(ciphertext, private_key)
        # Extract nonce and ciphertext from AES data
        nonce, encrypted_data = aes_data[:12], aes_data[12:]
        # Decrypt using AES
        return self.decrypt_with_aes(nonce, encrypted_data, shared_secret)

    def encrypt_model_weights(self, weights: Dict[str, Any], password: str = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Encrypt model weights using hybrid AES-Kyber encryption.

        Args:
            weights: Model weights dictionary
            password: Optional password for additional security layer

        Returns:
            Tuple of (encrypted_weights, encryption_metadata)
        """
        # Generate a Kyber keypair
        public_key, private_key = self.generate_kyber_keypair()
        
        # Use KMS if available, otherwise use password
        salt = os.urandom(16)
        if self.kms_key_arn and self._kms_client:
            # Generate a data key using KMS
            response = self._kms_client.generate_data_key(
                KeyId=self.kms_key_arn,
                KeySpec='AES_256'
            )
            plaintext_key = response['Plaintext']
            encrypted_key = response['CiphertextBlob']
        else:
            # Derive key from password
            plaintext_key = self._derive_key(password or self.client_id, salt)
            encrypted_key = None
        
        # Serialize weights to bytes
        weights_bytes = json.dumps(weights).encode()
        
        # Encrypt with AES first
        nonce, aes_ciphertext = self.encrypt_with_aes(weights_bytes, plaintext_key)
        
        # Then encrypt the AES key with Kyber
        kyber_ciphertext, _ = self.encrypt_with_kyber(plaintext_key, public_key)
        
        # Prepare encrypted weights
        encrypted_weights = {
            "encrypted_data": aes_ciphertext.hex(),
            "kyber_encrypted_key": kyber_ciphertext.hex(),
        }
        
        # Metadata needed for decryption
        encryption_metadata = {
            "nonce": nonce.hex(),
            "salt": salt.hex(),
            "kyber_public_key": public_key.hex(),
            "kyber_private_key": private_key.hex(),
            "kms_encrypted_key": encrypted_key.hex() if encrypted_key else None,
            "kms_key_arn": self.kms_key_arn,
        }
        
        return encrypted_weights, encryption_metadata

    def decrypt_model_weights(
        self, 
        encrypted_weights: Dict[str, Any], 
        encryption_metadata: Dict[str, Any], 
        password: str = None
    ) -> Dict[str, Any]:
        """
        Decrypt model weights using hybrid AES-Kyber encryption.

        Args:
            encrypted_weights: Encrypted model weights
            encryption_metadata: Metadata from encryption process
            password: Optional password matching the one used for encryption

        Returns:
            Decrypted model weights
        """
        # Convert hex strings back to bytes
        aes_ciphertext = bytes.fromhex(encrypted_weights["encrypted_data"])
        kyber_ciphertext = bytes.fromhex(encrypted_weights["kyber_encrypted_key"])
        nonce = bytes.fromhex(encryption_metadata["nonce"])
        salt = bytes.fromhex(encryption_metadata["salt"])
        private_key = bytes.fromhex(encryption_metadata["kyber_private_key"])
        
        # Get the AES key
        if encryption_metadata["kms_encrypted_key"] and self._kms_client:
            # Decrypt the data key using KMS
            encrypted_key = bytes.fromhex(encryption_metadata["kms_encrypted_key"])
            response = self._kms_client.decrypt(
                CiphertextBlob=encrypted_key,
                KeyId=encryption_metadata["kms_key_arn"]
            )
            aes_key = response['Plaintext']
        else:
            # Derive key from password
            aes_key = self._derive_key(password or self.client_id, salt)
        
        # Decrypt the model weights using AES
        decrypted_data = self.decrypt_with_aes(nonce, aes_ciphertext, aes_key)
        
        # Parse JSON and return
        return json.loads(decrypted_data.decode())

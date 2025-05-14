"""Service layer for cipher operations."""

from typing import Any

from ciphers.cipher_strategy import CipherFactory


class CipherService:
    """Service for encrypting and decrypting messages."""

    @staticmethod
    def encrypt(message: str, algorithm: str, key: Any) -> str:
        """
        Encrypt a message using the specified algorithm.

        Args:
            message: The message to encrypt
            algorithm: The name of the cipher algorithm
            key: The key for the cipher algorithm

        Returns:
            The encrypted message
        """
        cipher = CipherFactory.get_cipher(algorithm)
        return cipher.encrypt(message, key)

    @staticmethod
    def decrypt(message: str, algorithm: str, key: Any) -> str:
        """
        Decrypt a message using the specified algorithm.

        Args:
            message: The encrypted message
            algorithm: The name of the cipher algorithm
            key: The key for the cipher algorithm

        Returns:
            The decrypted message
        """
        cipher = CipherFactory.get_cipher(algorithm)
        return cipher.decrypt(message, key)

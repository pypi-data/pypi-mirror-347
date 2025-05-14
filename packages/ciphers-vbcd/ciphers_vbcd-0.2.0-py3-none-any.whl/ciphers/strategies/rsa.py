"""RSA cipher implementation."""

import base64
from typing import Union

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
except ImportError as err:
    raise ImportError(
        "The 'cryptography' package is required for RSA encryption. "
        "Please install it with 'pip install ciphers-vbc[rsa]'"
    ) from err

from ciphers.cipher_strategy import CipherStrategy


class RSACipher(CipherStrategy):
    """Implementation of RSA public key encryption algorithm."""

    def encrypt(self, message: str, key: Union[str, bytes]) -> str:
        """
        Encrypt a message using an RSA public key.

        Args:
            message: The plaintext message to encrypt
            key: The public key in PEM format (string or bytes)

        Returns:
            Base64-encoded encrypted message
        """
        # Convert string key to bytes if needed
        if isinstance(key, str):
            key = key.encode()

        # Load the public key
        public_key = serialization.load_pem_public_key(key)

        # Ensure it's an RSA public key
        if not isinstance(public_key, RSAPublicKey):
            raise ValueError("The provided key is not an RSA public key")

        # Encrypt the message
        ciphertext = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Return base64 encoded ciphertext
        return base64.b64encode(ciphertext).decode()

    def decrypt(self, message: str, key: Union[str, bytes]) -> str:
        """
        Decrypt a message using an RSA private key.

        Args:
            message: The base64-encoded encrypted message
            key: The private key in PEM format (string or bytes)

        Returns:
            Decrypted plaintext message
        """
        # Convert string key to bytes if needed
        if isinstance(key, str):
            key = key.encode()

        # Load the private key
        private_key = serialization.load_pem_private_key(key, password=None)

        # Ensure it's an RSA private key
        if not isinstance(private_key, RSAPrivateKey):
            raise ValueError("The provided key is not an RSA private key")

        # Type assertion for mypy
        private_key_rsa: RSAPrivateKey = private_key

        # Decode the base64 ciphertext
        ciphertext = base64.b64decode(message)

        # Decrypt the message
        plaintext = private_key_rsa.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return plaintext.decode()

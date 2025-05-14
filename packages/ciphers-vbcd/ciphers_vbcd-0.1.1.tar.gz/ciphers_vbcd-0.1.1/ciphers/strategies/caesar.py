"""Caesar cipher implementation."""

from ciphers.cipher_strategy import CipherStrategy


class CaesarCipher(CipherStrategy):
    """Implementation of the Caesar cipher algorithm."""

    def encrypt(self, message: str, key: int) -> str:
        """
        Encrypt a message using the Caesar cipher.

        Args:
            message: The message to encrypt
            key: The shift value (integer)

        Returns:
            The encrypted message
        """
        result = ""
        for char in message:
            if char.isalpha():
                ascii_offset = ord("A") if char.isupper() else ord("a")
                # Convert to 0-25, shift, and convert back to ASCII
                shifted = (ord(char) - ascii_offset + int(key)) % 26 + ascii_offset
                result += chr(shifted)
            else:
                result += char
        return result

    def decrypt(self, message: str, key: int) -> str:
        """
        Decrypt a message using the Caesar cipher.

        Args:
            message: The encrypted message
            key: The shift value (integer)

        Returns:
            The decrypted message
        """
        # Decryption is just encryption with the negative key
        return self.encrypt(message, -int(key))

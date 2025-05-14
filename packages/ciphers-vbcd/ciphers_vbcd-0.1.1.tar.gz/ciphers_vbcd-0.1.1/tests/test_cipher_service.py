"""Tests for the cipher service."""

import unittest

from ciphers.cipher_service import CipherService


class TestCipherService(unittest.TestCase):
    """Test cases for the cipher service."""

    def test_encrypt_caesar(self) -> None:
        """Test encryption with the Caesar cipher through the service."""
        result = CipherService.encrypt("Hello, World!", "caesar", 3)
        self.assertEqual(result, "Khoor, Zruog!")

    def test_decrypt_caesar(self) -> None:
        """Test decryption with the Caesar cipher through the service."""
        result = CipherService.decrypt("Khoor, Zruog!", "caesar", 3)
        self.assertEqual(result, "Hello, World!")

    def test_invalid_algorithm(self) -> None:
        """Test that an invalid algorithm raises a ValueError."""
        with self.assertRaises(ValueError):
            CipherService.encrypt("Hello", "invalid_algorithm", "key")


if __name__ == "__main__":
    unittest.main()

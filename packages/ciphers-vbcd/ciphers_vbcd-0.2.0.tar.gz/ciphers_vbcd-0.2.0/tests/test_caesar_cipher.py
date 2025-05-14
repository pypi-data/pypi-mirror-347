"""Tests for the Caesar cipher implementation."""

import unittest

from ciphers.strategies.caesar import CaesarCipher


class TestCaesarCipher(unittest.TestCase):
    """Test cases for the Caesar cipher."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.cipher = CaesarCipher()

    def test_encrypt(self) -> None:
        """Test encryption with the Caesar cipher."""
        self.assertEqual(self.cipher.encrypt("hello", 3), "khoor")
        self.assertEqual(self.cipher.encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(self.cipher.encrypt("Hello, World!", 3), "Khoor, Zruog!")
        self.assertEqual(self.cipher.encrypt("xyz", 3), "abc")

    def test_decrypt(self) -> None:
        """Test decryption with the Caesar cipher."""
        self.assertEqual(self.cipher.decrypt("khoor", 3), "hello")
        self.assertEqual(self.cipher.decrypt("KHOOR", 3), "HELLO")
        self.assertEqual(self.cipher.decrypt("Khoor, Zruog!", 3), "Hello, World!")
        self.assertEqual(self.cipher.decrypt("abc", 3), "xyz")


if __name__ == "__main__":
    unittest.main()

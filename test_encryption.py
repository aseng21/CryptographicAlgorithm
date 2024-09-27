"""Unit tests for the Feistel cipher implementation."""

import unittest
from main import CipherTest


class TestEncryption(unittest.TestCase):
    """Test cases for encryption and decryption functionality."""

    def setUp(self):
        # Test parameters
        self.message = "Hello, World!"
        self.prime = 61  # Prime for good mixing
        self.key = 17    # Any number works
        self.rounds = 10  # More rounds = more secure
        self.box_size = 256   # Substitution box size
        
        # Create our test cipher
        self.cipher = CipherTest(
            prime=self.prime,
            key=self.key,
            rounds=self.rounds,
            box_size=self.box_size
        )

    def test_encryption_decryption(self):
        # Make sure we can recover our message
        encrypted, _ = self.cipher.test_encryption(self.message)
        decrypted, _ = self.cipher.test_decryption(encrypted)
        self.assertEqual(self.message, decrypted.strip())


if __name__ == "__main__":
    unittest.main()
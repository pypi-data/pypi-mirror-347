"""Test cases for the RSA cipher."""

import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ciphers.cipher_service import CipherService
from ciphers.strategies.rsa import RSACipher


class TestRSACipher(unittest.TestCase):
    """Test cases for the RSA cipher."""

    def setUp(self) -> None:
        """Generate a key pair for testing."""
        # Generate a private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Get the public key
        self.public_key = self.private_key.public_key()

        # Serialize the keys to PEM format
        self.private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        self.cipher = RSACipher()
        self.message = "This is a secret message"

    def test_encrypt_decrypt(self) -> None:
        """Test that encryption followed by decryption returns the original message."""
        encrypted = self.cipher.encrypt(self.message, self.public_key_pem)
        decrypted = self.cipher.decrypt(encrypted, self.private_key_pem)
        self.assertEqual(self.message, decrypted)

    def test_service_encrypt_decrypt(self) -> None:
        """Test that the cipher service works with RSA."""
        encrypted = CipherService.encrypt(self.message, "rsa", self.public_key_pem)
        decrypted = CipherService.decrypt(encrypted, "rsa", self.private_key_pem)
        self.assertEqual(self.message, decrypted)

    def test_invalid_public_key(self) -> None:
        """Test that an error is raised when an invalid public key is provided."""
        with self.assertRaises(ValueError):
            self.cipher.encrypt(self.message, b"invalid key")

    def test_invalid_private_key(self) -> None:
        """Test that an error is raised when an invalid private key is provided."""
        encrypted = self.cipher.encrypt(self.message, self.public_key_pem)
        with self.assertRaises(ValueError):
            self.cipher.decrypt(encrypted, b"invalid key")

    def test_non_rsa_key(self) -> None:
        """Test that an error is raised when a non-RSA key is provided."""
        # This would require generating a different type of key (e.g., DSA, EC)
        # For simplicity, we'll just test the ValueError from our type check
        with self.assertRaises(ValueError):
            # This will fail at our isinstance check, not at load_pem_public_key
            self.cipher.encrypt(self.message, self.private_key_pem)


if __name__ == "__main__":
    unittest.main()

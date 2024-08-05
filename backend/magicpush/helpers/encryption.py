import jwt
import json
import time
import base64
import ecdsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


class Encryption(object):

    @staticmethod
    def generate_vapid_keys():
        """
        Generate a new set of encoded key-pair for VAPID
        """

        pk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        vk = pk.get_verifying_key()

        # Encode the private key in URL-safe Base64 format and remove padding
        private_key_encoded = base64.urlsafe_b64encode(pk.to_string()).decode('utf-8').rstrip('=')
        # Prefix public key with \x04 (uncompressed point prefix), encode it, and remove padding
        public_key_uncompressed = b"\x04" + vk.to_string()
        public_key_encoded = base64.urlsafe_b64encode(public_key_uncompressed).decode('utf-8').rstrip('=')

        return private_key_encoded, public_key_encoded

    # @staticmethod
    # def generate_vapid_keys():
    #     # Generate a private key for use in the signing algorithm.
    #     private_key = ec.generate_private_key(
    #         ec.SECP256R1(), default_backend()
    #     )
    #
    #     # Serialize private key to PEM format
    #     private_pem = private_key.private_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PrivateFormat.PKCS8,
    #         encryption_algorithm=serialization.NoEncryption()
    #     )
    #
    #     # Generate public key
    #     public_key = private_key.public_key()
    #     public_pem = public_key.public_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PublicFormat.SubjectPublicKeyInfo
    #     )
    #
    #     return private_pem.decode('utf-8'), public_pem.decode('utf-8')

    @staticmethod
    def decode_keys_from_urlsafe_base64(private_key_encoded, curve=ecdsa.NIST256p):
        """
        Decode URL-safe Base64 encoded ECDSA private key back to a key object.

        Args:
        private_key_encoded (str): The URL-safe Base64 encoded private key string.
        curve: The ECDSA curve used for the key generation (default is NIST256p).

        Returns:
        ecdsa.SigningKey: The ECDSA private key object.
        """
        private_key_bytes = base64.urlsafe_b64decode(private_key_encoded + '==')
        private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=curve)
        return private_key

    @staticmethod
    def create_jwt(private_key, subject, audience, expiration):
        # Load the private key from PEM formatted string
        private_key_pem = Encryption.decode_keys_from_urlsafe_base64(private_key).to_pem()

        # Create a payload for the JWT
        payload = {
            'sub': subject,
            'aud': audience,
            'exp': expiration
        }

        # Encode a JWT using the ES256 algorithm
        token = jwt.encode(
            payload,
            private_key_pem,
            algorithm='ES256'
        )

        return token

    @staticmethod
    def urlsafe_public_key(public_key):
        public_key_uncompressed = b"\x04" + str(public_key).encode('utf-8')
        public_key_encoded = base64.urlsafe_b64encode(public_key_uncompressed).decode('utf-8').rstrip('=')
        return public_key_encoded

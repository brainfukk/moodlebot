from cryptography.fernet import Fernet

from src.core.config import SECRET_KEY


def encrypt_password(password: bytes) -> bytes:
    return Fernet(SECRET_KEY).encrypt(password)


def decrypt_password(password: bytes) -> bytes:
    return Fernet(SECRET_KEY).decrypt(password)

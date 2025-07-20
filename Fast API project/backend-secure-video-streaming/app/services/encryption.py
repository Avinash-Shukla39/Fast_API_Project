from cryptography.fernet import Fernet
from app.config import Config

def encrypt_data(data: bytes) -> bytes:
    fernet = Fernet(Config.ENCRYPTION_KEY.encode())
    return fernet.encrypt(data)

def decrypt_data(encrypted_data: bytes) -> bytes:
    fernet = Fernet(Config.ENCRYPTION_KEY.encode())
    return fernet.decrypt(encrypted_data)
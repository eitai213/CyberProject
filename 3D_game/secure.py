import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from random import randbytes
import os

def generate_keys_for_rsa():
    (public_key, private_key) = rsa.newkeys(2048)
    return private_key, public_key

def encrypt_key(public_key, message):
    encrypted_message = rsa.encrypt(message, public_key)
    return encrypted_message

def decrypt_key(private_key, encrypted_message):
    decrypted_message = rsa.decrypt(encrypted_message, private_key)
    return decrypted_message

def encrypt_message(key, message):
    iv = os.urandom(16)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_message

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

def create_aes_key():
    key = os.urandom(32)
    return key


if __name__ == "__main__":
    private_key, public_key = generate_keys_for_rsa()
    aes_key = randbytes(32)
    encrypted_key = encrypt_key(public_key, aes_key)
    decrypted_key = decrypt_key(private_key, encrypted_key)

    message = "Hello, World!"
    encrypted_message = encrypt_message(aes_key, message)
    decrypted_message = decrypt_message(aes_key, encrypted_message)

    assert aes_key == decrypted_key, "AES keys do not match!"
    assert message == decrypted_message, "Messages do not match!"

    print("All tests passed!!!!!!!!!!!!!!!")

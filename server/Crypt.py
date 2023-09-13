from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

class Crypt():
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        if isinstance(data, str):  
            data_to_encrypt = data.encode()

            # Pad the data to a multiple of 16 bytes using PKCS#7 padding
            block_size = 16
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data_to_encrypt) + padder.finalize()

            # Create an AES object with the key and mode (ECB)
            cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()

            # Encrypt the data
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Convert the encrypted data to bytes (since the encrypted data may contain non-ASCII characters)
            encrypted_data_bytes = bytes(encrypted_data)

            # Send the encrypted data to the MicroPython device via a communication channel (e.g., serial)
            return encrypted_data_bytes
        else:
            raise ValueError("data should be a string")

    def decrypt(self, data):
        if isinstance(data, bytes):
            encrypted_data_bytes = data
            # Create an AES object with the key and mode (ECB)
            cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt the data
            decrypted_data = decryptor.update(encrypted_data_bytes) + decryptor.finalize()

            # Remove PKCS#7 padding
            def unpad_pkcs7(data):
                pad_length = data[-1]
                return data[:-pad_length]

            data_to_decrypt = unpad_pkcs7(decrypted_data)

            # Convert decrypted data to string (assuming it was originally encoded as a string in MicroPython)
            decrypted_string = data_to_decrypt.decode()
            return decrypted_string
        else:
            raise ValueError("data must be in bytes")

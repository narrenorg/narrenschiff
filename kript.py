import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AES256Cipher:

    def __init__(self, password, salt):
        self.password = password.encode('utf-8')
        self.salt = salt.encode('utf-8')

        self.backend = default_backend()
        self.key = self.pbkdf2()

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )

        encryptor = cipher.encryptor()
        padder = padding.PKCS7(256).padder()
        plaintext = plaintext.rstrip().encode('utf-8')
        padded = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
        return base64.b64encode(iv + ciphertext)

    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext.rstrip())
        # iv = ciphertext[:16]
        iv, ciphertext = ciphertext[:16], ciphertext[16:]
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )

        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(256).unpadder()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        unpadded = unpadder.update(plaintext) + unpadder.finalize()
        return unpadded.decode('utf-8')

    def pbkdf2(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32, salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(self.password)

password = 'dummy_password'
salt = 'IU^7862390rZI)&(*hi23q2rfbnO(*^$%#'
cipher = AES256Cipher(password, salt)

ct = cipher.encrypt('secret_string')
print(cipher.decrypt(ct))

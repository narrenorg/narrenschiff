# Copyright 2021 The Narrenschiff Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import base64

import yaml
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AES256Cipher:
    """Encode and/or decode strings."""

    def __init__(self, keychain):
        """
        Construct :class:`narrenschiff.chest.AES256Cypher`.

        :param keychain: Object containing key and spice
        :type keychain: :class:`narrenschiff.chest.Keychain`
        :return: Void
        :rtype: ``None``
        """
        self.password = keychain.key.encode('utf-8')
        self.salt = keychain.spice.encode('utf-8')

        self.backend = default_backend()
        self.key = self.pbkdf2()

    def encrypt(self, plaintext):
        """
        Encrypt plaintext.

        :param plaintext: Plaintext
        :type plaintext: ``str``
        :return: Ciphertext
        :rtype: ``str``
        """
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
        """
        Decrypt ciphertext.

        :param ciphertext: Ciphertext
        :type ciphertext: ``str``
        :return: Plaintext
        :rtype: ``str``
        """
        ciphertext = base64.b64decode(ciphertext.rstrip())
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
        """
        Derive a 32 bytes (256 bits) key.

        :return: Password hash
        :rtype: ``byte string``
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(self.password)


class Chest:
    """Manipulate chest file."""

    def __init__(self, keychain, path):
        """
        Unlock treasure chest.

        :param keychain: Object containing key and spice
        :type keychain: :class:`narrenschiff.chest.Keychain`
        :param path: Path to the chest file
        :type path: ``str``
        :return: Void
        :rtype: ``None``
        """
        self.keychain = keychain
        self.path = path
        self.chest = self.load_chest_file()

    def load_chest_file(self):
        """
        Load chest file with encrypted values.

        :return: Serialized YAML object
        :rtype: ``dict``
        """
        with open(self.path, 'r') as f:
            chest = yaml.safe_load(f)
        return chest if chest else {}

    def update(self, variable, value):
        """
        Add or update chest file.

        :param variable: Variable name to update
        :type variable: ``str``
        :param value: Value of the variable
        :type value: ``str``
        :return: Void
        :rtype: ``None``
        """
        cipher = AES256Cipher(self.keychain)
        self.chest[variable] = cipher.encrypt(value).decode('utf-8')

        with open(self.path, 'w') as f:
            f.write(yaml.dump(self.chest))

    def show(self, variable):
        """
        Show decrypted value of the variable.

        :param variable: Variable name
        :type variable: ``str``
        :param value: Value of the variable
        :type value: ``str``
        :return: Decrypted value
        :rtype: ``str``
        """
        cipher = AES256Cipher(self.keychain)
        return cipher.decrypt(self.chest[variable])

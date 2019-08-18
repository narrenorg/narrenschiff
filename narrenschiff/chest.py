import os
import yaml
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ChestException(Exception):
    """Use when anything goes wrong with encryption process."""

    pass


class Keychain:
    """Bundle password and salt."""

    def __init__(self):
        conf = self.load_configuration_file()
        self.key = self.load_value(conf.get('key'))
        self.spice = self.load_value(conf.get('spice'))

    def load_value(self, path):
        """
        Load value from file on the given path.

        :param path: Path to the file
        :type path: ``str``
        """
        with open(path, 'r') as f:
            secret = f.readlines()[0]
        return secret.rstrip()

    def load_configuration_file(self):
        """
        Load ``.narrenschiff.yaml`` configuration file.
        """
        path = self.get_configuration_path()
        with open(path, 'r') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf

    def get_configuration_path(self):
        """
        Get path to the existing configuration file.

        :return: Path to configuraiton file
        :rtype: ``str``
        """
        project = os.path.dirname(os.path.abspath(__file__))  # os.getcwd()
        project_root = os.path.abspath(os.path.join(project, os.pardir))
        narrenschiff = os.path.join(project_root, '.narrenschiff')

        narrenschiff_yaml = '.'.join([narrenschiff, 'yaml'])
        narrenschiff_yml = '.'.join([narrenschiff, 'yml'])

        conf_yaml = self.check_configuration_file_exists(narrenschiff_yaml)
        conf_yml = self.check_configuration_file_exists(narrenschiff_yml)

        if bool(conf_yaml) != bool(conf_yml):
            return conf_yaml or conf_yml

        exception = 'Ambiguous configuration. Either missing or duplicated'
        raise ChestException(exception)

    def check_configuration_file_exists(self, path):
        """
        Check if configuraiton file exists. If it exists, return its path.

        :param path: Path to configuration file
        :type path: ``str``
        :return: Path
        :rtype: ``str``
        """
        if os.path.isfile(path):
            return path
        return ''


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
            chest = yaml.load(f, Loader=yaml.FullLoader)
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

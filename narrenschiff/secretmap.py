import os
import yaml
import uuid
import shutil
from contextlib import suppress

from narrenschiff.chest import AES256Cipher
from narrenschiff.common import Singleton


class CourseLocationError(Exception):
    pass


class SecretmapCommand(metaclass=Singleton):
    """Manage secret maps. Secret maps are paths to encrypted files."""

    FILENAME = 'secretmap.yaml'

    def __init__(self, keychain, directory):
        """
        Construct a :class:`narrenschiff.secretmap.SecretmapCommand`.

        :param keychain: Keychain contains key and spice
        :type keychain: :class:`narrenschiff.chest.Keychain`
        :param directory: Path to directory containing secretmap
        :type directory: ``str``
        :return: Void
        :rtype: ``None``
        """
        if os.path.isfile(directory):
            self.directory = os.path.dirname(directory)
        elif os.path.isdir(directory):
            self.directory = directory
        else:
            raise CourseLocationError

        self.filepath = os.path.join(directory, SecretmapCommand.FILENAME)
        self.keychain = keychain
        self.tmp = os.path.join('/tmp', str(uuid.uuid4()))

    def upsert(self, src, dest, treasure):
        """
        Encrypts file and inserts data to config file.

        :param src: Source filepath for encryption
        :type src: ``str``
        :param dest: Destination filepath of the encrypted file
        :type dest: ``str``
        :param treasure: Name of the variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        with open(src, 'r') as f:
            cipher = AES256Cipher(self.keychain)
            enc_file_core = cipher.encrypt(f.read()).decode('utf-8')

        dest_abspath = os.path.abspath(os.path.join(self.directory, dest))
        try:
            os.mkdir(os.path.dirname(dest_abspath), 0o755)
        except FileExistsError:
            pass

        with open(dest_abspath, 'w') as f:
            f.write(enc_file_core)

        config = self._read_config()
        config[treasure] = dest
        self._write_config(config)

    def decrypt(self, dest, treasure):
        """
        Decrypts file and stores it to given destination.

        :param dest: Destination filepath of the decrypted file
        :type dest: ``str``
        :param treasure: Name of the variable
        :type treasure: ``str``
        :return: Void
        :rtype: ``None``
        """
        config = self._read_config()
        src = os.path.abspath(os.path.join(self.directory, config[treasure]))

        with open(src, 'r') as f:
            cipher = AES256Cipher(self.keychain)
            enc_file_core = cipher.decrypt(f.read())

        with open(dest, 'w') as f:
            f.write(enc_file_core)

    def render_all_files(self):
        """
        Decrypt and copy all files at the given destination.
        """
        os.makedirs(self.tmp)
        for key, value in self._read_config().items():
            basepath = os.path.dirname(value)

            with suppress(FileExistsError):
                os.makedirs(os.path.join(self.tmp, basepath))

            destination = os.path.join(self.tmp, value)
            if not os.path.exists(destination):
                self.decrypt(destination, key)

    def clear_all_files(self):
        """
        Delete all decrypted files.

        :return: Void
        :rtype: ``None``
        """
        shutil.rmtree(self.tmp)

    def _read_config(self):
        with open(self.filepath, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config if config else {}

    def _write_config(self, config):
        with open(self.filepath, 'w') as f:
            f.write(yaml.dump(config))

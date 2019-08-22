from .chest import AES256Cipher
import os
import yaml

class CourseLocationError(Exception):
    pass

class SecretmapCommand:

    FILENAME = 'secretmap.yaml'

    def __init__(self, keychain, directory):
        if os.path.isfile(directory):
            self.directory = os.path.dirname(directory)
        elif os.path.isdir(directory):
            self.directory = directory
        else:
            raise CourseLocationError

        self.filepath = os.path.join(directory, SecretmapCommand.FILENAME)
        self.keychain = keychain

    def upsert(self, src, dest, treasure):
        """
        Encrypts file and inserts data to config file
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
        config[treasure] = dest_abspath
        self._write_config(config)

    def decrypt(self, dest, treasure):
        """
        Decrypts file and stores it to given destination
        """
        config = self._read_config()
        src_abspath = config[treasure]

        with open(src_abspath, 'r') as f:
            cipher = AES256Cipher(self.keychain)
            enc_file_core = cipher.decrypt(f.read())

        with open(dest, 'w') as f:
            f.write(enc_file_core)

    def _read_config(self):
        with open(self.filepath, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def _write_config(self, config):
        with open(self.filepath, 'w') as f:
            f.write(yaml.dump(config))

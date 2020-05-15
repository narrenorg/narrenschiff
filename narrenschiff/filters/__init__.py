import os
import base64


def b64enc(value):
    """
    Encode a string using base64.

    :param value: Text to be encoded
    :type value: ``str``
    :return: Encoded text
    :rtype: ``str``

    Use this filter for k8s secrets. Values for the secrets need to be encoded
    before the ``Secret`` resource is deployed to k8s.
    """
    return base64.b64encode(value.encode('utf-8')).decode('ASCII')


def rtrim(value):
    """
    Strip trailing whitespace.

    :param value: Text to be processed
    :type value: ``str``
    :return: Text without trailing whitespace
    :rtype: ``str``
    """
    return value.rstrip()


def secretmap(value):
    """
    Label path with ``{{secretmap}}``.

    :param value: Path
    :type value: ``str``
    :return: Labeled path
    :rtype: ``str``
    """
    return os.path.join('{{secretmap}}', value)


filters = {
    'b64enc': b64enc,
    'rtrim': rtrim,
    'secretmap': secretmap,
}

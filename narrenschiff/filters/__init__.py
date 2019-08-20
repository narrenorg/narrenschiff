import base64


def b64enc(value):
    """
    Encode a string using base64.

    :param value: Text to be encoded
    :type value: ``str``
    :return: Encoded text
    :rtype: ``str``
    """
    return base64.b64encode(value.encode('utf-8')).decode('ASCII')

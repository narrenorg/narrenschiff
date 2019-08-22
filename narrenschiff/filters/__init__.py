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


def rtrim(value):
    """
    Strip trailing whitespace.

    :param value: Text to be processed
    :type value: ``str``
    :return: Text without trailing whitespace
    :rtype: ``str``
    """
    return value.rstrip()


filters = {
    'b64enc': b64enc,
    'rtrim': rtrim,
}

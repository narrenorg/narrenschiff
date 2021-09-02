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


def b64enc(value):
    """
    Encode a string using base64.

    :param value: Text to be encoded
    :type value: ``str``
    :return: Encoded text
    :rtype: ``str``

    Use this filter for k8s secrets. Values for secrets need to be encoded
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

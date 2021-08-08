# Copyright 2021 Petar Nikolovski

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
from setuptools import setup
from setuptools import find_packages

import narrenschiff


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme:
    README = readme.read()


setup(
    name='narrenschiff',
    version=narrenschiff.__version__,
    packages=find_packages(),
    description='k8s deployment and configuration management tool',
    long_description=README,
    license_files=('LICENSE',),
    license='Apache License, Version 2.0',
    url='https://example.com',
    maintainer='Petar Nikolovski',
    maintainer_email='petar.nikolovski@protonmail.com',
    install_requires=[
        'click', 'PyYAML', 'Jinja2', 'cryptography', 'colorlog'
    ],
    entry_points="""
        [console_scripts]
        narrenschiff=narrenschiff.narrenschiff:narrenschiff
    """,
)

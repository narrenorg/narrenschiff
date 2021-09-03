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
from setuptools import setup
from setuptools import find_packages

import narrenschiff


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme:
    README = readme.read()


setup(
    name='narrenschiff',
    version=narrenschiff.__version__,
    packages=find_packages('.', exclude=['tests*', 'docs*']),
    description='Configuration management tool for Kubernetes',
    long_description=README,
    long_description_content_type='text/markdown',
    license_files=('LICENSE',),
    license='Apache License, Version 2.0',
    url='https://narrenschiff.xyz',
    project_urls={
        'Documentation': 'https://docs.narrenschiff.xyz',
        'Source': 'https://github.com/narrenorg/narrenschiff',
    },
    maintainer='Petar Nikolovski',
    maintainer_email='petar.nikolovski@protonmail.com',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Topic :: Utilities'
    ],
    install_requires=[
        'click', 'PyYAML', 'Jinja2', 'cryptography', 'colorlog'
    ],
    entry_points="""
        [console_scripts]
        narrenschiff=narrenschiff.narrenschiff:narrenschiff
    """,
)

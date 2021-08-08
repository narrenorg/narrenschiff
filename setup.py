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

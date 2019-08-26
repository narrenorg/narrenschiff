import os
from setuptools import setup
from setuptools import find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme:
    README = readme.read()


setup(
    name='narrenschiff',
    version=os.getenv('CI_COMMIT_TAG'),
    packages=find_packages(),
    description='k8s deployment and configuration management tool',
    long_description=README,
    url='https://example.com',
    maintainer='Petar Nikolovski',
    maintainer_email='nikolovski@brainshuttle.com',
    install_requires=[
        'click', 'PyYAML', 'Jinja2', 'cryptography'
    ],
    entry_points="""
        [console_scripts]
        narrenschiff=narrenschiff.narrenschiff:narrenschiff
    """,
)

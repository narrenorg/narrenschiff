from setuptools import setup

setup(
    name='narrenschiff',
    version='0.0.1',
    py_modules=['narrenschiff'],
    install_requires=[
        'Click', 'PyYAML'
    ],
    entry_points="""
        [console_scripts]
        narrenschiff=narrenschiff.narrenschiff:narrenschiff
    """,
)

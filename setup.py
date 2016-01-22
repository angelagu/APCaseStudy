try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'AlphaParity Coding Challenge',
    'author': 'Angela Gu',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'alpha_parity'
}

setup(**config)
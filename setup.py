from setuptools import setup

setup(
    name = 'wikid',
    version = '0.0.1',
    packages = ['wikid'],
    package_data = { 'wikid': ['data/js/*', 'data/css/*'] },
    scripts = ['scripts/wikid'],
    install_requires = ['markdown'],
    description = 'A stupid-simple, file-based wiki.',
    author = 'Elisha Cook',
    author_email = 'elisha@elishacook.com'
)
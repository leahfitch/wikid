from distutils.core import setup

setup(
    name = 'wikid',
    version = '0.0.2',
    packages = ['wikid'],
    package_data = { 'wikid': ['data/js/*', 'data/css/*'] },
    scripts = ['scripts/wikid'],
    requires = ['markdown'],
    description = 'A stupid-simple, file-based wiki.',
    author = 'Elisha Cook',
    author_email = 'elisha@elishacook.com'
)
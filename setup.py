from setuptools import setup

setup(
    name = 'wikid',
    version = '0.0.2',
    packages = ['wikid'],
    data_files = [
    	('wikid/data/css', ['wikid/data/css/styles.css']),
    	('wikid/data/js', ['wikid/data/js/jquery.js']),
    	('wikid/data/js', ['wikid/data/js/search.js'])
    ],
    scripts = ['scripts/wikid'],
    install_requires = ['markdown'],
    description = 'A stupid-simple, file-based wiki.',
    author = 'Elisha Cook',
    author_email = 'elisha@elishacook.com'
)
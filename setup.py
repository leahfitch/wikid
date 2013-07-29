from distutils.core import setup

setup(
    name = 'wikid',
    version = '0.0.10',
    packages = ['wikid'],
    package_data = { 'wikid': ['data/js/*', 'data/css/*'] },
    scripts = ['scripts/wikid'],
    requires = ['markdown'],
    description = 'A stupid-simple, file-based wiki.',
    author = 'Elisha Cook',
    author_email = 'elisha@elishacook.com',
    url = 'http://github.com/elishacook/wikid/',
    license = 'MIT',
    classifiers = [
    	'Development Status :: 4 - Beta',
    	'Intended Audience :: Developers',
    	'Environment :: Console',
	    'Environment :: Web Environment',
    	'License :: OSI Approved :: MIT License',
    	'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)

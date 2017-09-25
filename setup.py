try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'describe the project',
	'author': 'David Julian',
	'url': 'git location',
	'download_url': 'git download location',
	'author_email': 'david.julian@asu.edu',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['NAME'],
	'scripts': [],
	'name': 'projectname'
}

setup(**config)
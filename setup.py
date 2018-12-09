from distutils.core import setup
setup(
	name='oldschoolstats',
	version='1.0.0.1',
	description='',
	author='Bernd van der Wielen',
	url='',
	packages=['oldschoolstats'],
	install_requires=[
		'requests',
		'beautifulsoup4',                       
	],
	include_package_data=True
)
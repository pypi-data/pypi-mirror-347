from setuptools import setup

setup(
	name='thrilltiger_scanner',
	version='0.1',
	packages=['portscanner'],
	install_requires=[],
	entry_points={
		'console_scripts': [
			'portscanner = portscanner.portscanner:main'
		]
	}
)

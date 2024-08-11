from setuptools import setup, find_packages
setup(
    name='gdrive',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gdrive=gdrive_cli.main:cli',
        ],
    },
)
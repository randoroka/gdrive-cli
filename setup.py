from setuptools import setup

setup(
    name='gdrive',
    version='0.1.0',
    py_modules=['main'],
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
            'gdrive=main:cli',
        ],
    },
)

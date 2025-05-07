from setuptools import setup, find_packages

import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(HERE, 'README.md')
CHANGELOG_PATH = os.path.join(HERE, 'CHANGELOG.md')

if not (sys.version_info.major == 3):
    raise RuntimeError('Wrong Python version')

README = open(README_PATH, encoding='utf-8').read()
CHANGELOG = open(CHANGELOG_PATH, encoding='utf-8').read()

setup(
    name='ioacollector',
    url='https://github.com/0xRekejohn/IOACollector',
    author='0xRekejohn',
    author_email='info@johnrequejo.com'
    version='0.1',
    description="IOACollector is a tool that interacts with CrowdStrike's API to create, enable, delete, and manage IOA (Indicators of Attack) rules within specified rule groups.",
    long_description=README + '\n\n\'' + CHANGELOG,
    keywords='IOACollector, 0xRekejohn, CrowdStrike-API',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    install_requires=[
        'requests==2.31.0',
        'argparse==1.4.0',
        'getenv==0.2.0',
        'dotenv==0.9.9',
        'validators==0.34.0'
        ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ioacollector-add=ioacollector.main:create',
            'ioacollector-delete=ioacollector.main:delete',
            'ioacollector-config=ioacollector.main:configure'
        ],
    },
)
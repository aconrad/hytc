import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.1.0'

README = read('README.rst')
CHANGES = read('CHANGES.rst')

requires = [
    'click>=4.0',
    'pymongo',
    'pyteamcity',
]

setup(
    name="hytc",
    version=version,
    author="Alex Conrad",
    author_email="alexandre@surveymonkey.com",
    maintainer="Alex Conrad",
    maintainer_email="alexandre@surveymonkey.com",
    description="A TeamCity collector for Hygieia",
    license="MIT License",
    keywords="hygieia teamcity collector",
    url="https://github.com/SurveyMonkey/hytc",
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    long_description='%s\n\n%s' % (README, CHANGES),
    setup_requires=['setuptools_git'],
    install_requires=requires,
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4"
    ],
    entry_points={
        'console_scripts': [
            'hytc=hytc.cli:hytc',
        ],
    },
)

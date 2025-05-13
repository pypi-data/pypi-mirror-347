from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.0'

setup(
    name="scmethq",  # package name
    version=VERSION,  # package version
    description='scMethQ',  # package description
    packages=find_packages(),
    zip_safe=False,
)
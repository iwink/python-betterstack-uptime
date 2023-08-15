from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='betterstack-uptime',
    packages=find_packages(include=['betterstack.uptime']),
    version='1.0.0',
    author='iWink',
    author_email='hosting@iwink.nl',
    description='Library for communicating with the BetterStack Uptime API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwink/python-betterstack-uptime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Licence :: OSI Approved :: MIT Licence",
        "Operating System :: OS Independent",
        "Licence :: OSI Approved :: GNU General Public Licence v3 (GPLv3)",
    ],
    python_requires='>=3',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
)

from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='betterstack-uptime',
    packages=find_packages(include=['betterstack', 'betterstack.uptime', 'betterstack.uptime.*']),
    version='1.0.2',
    author='iWink',
    author_email='hosting@iwink.nl',
    description='Library for communicating with the BetterStack Uptime API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwink/python-betterstack-uptime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
)

from setuptools import find_packages, setup

setup(
    name='betterstack-uptime',
    packages=find_packages(include=['betterstack.uptime']),
    version='0.1.0',
    author='Wouter Mellema',
    author_email='w.mellema@iwink.nl',
    description='Library for communicating with the BetterStack Uptime API',
    long_description_content_type="text/markdown",
    url="https://github.om/iwink/betterstack-uptime",
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


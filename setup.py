from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Collection of reusable classes/functions used in several projects'

# Setting up
setup(
    name="common-shared-library",
    version=VERSION,
    author="Addenergyx (David Adeniji)",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['anticaptchaofficial', 'boto3', 'imessage-reader', 'selenium', 'webdriver-manager'],
    keywords=['python'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

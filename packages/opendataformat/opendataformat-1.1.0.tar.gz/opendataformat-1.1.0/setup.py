# setup.py

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='opendataformat',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,  # Include package data specified in MANIFEST.in
    package_data={
        'opendataformat': ['data/*.zip'],  # Include specific files
    },
    install_requires=[
        'pandas',
    ],
    description='The Open Data Format (ODF) is a new, non-proprietary, multilingual, metadata enriched, and zip-compressed data format with metadata structured in the Data Documentation Initiative (DDI) Codebook standard. This package allows reading and writing of data files in the Open Data Format (ODF) in pandas, and displaying metadata in different languages. For further information on the Open Data Format, see <https://opendataformat.github.io/>.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='opendataformat-team',
    author_email='opendataformat-team@diw.de',
    url='https://opendataformat.github.io/python-package',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

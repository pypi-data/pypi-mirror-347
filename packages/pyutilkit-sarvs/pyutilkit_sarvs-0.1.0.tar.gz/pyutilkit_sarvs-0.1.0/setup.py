"""
PyUtilKit package setup file.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Extract version from pyutilkit/__init__.py
with open(os.path.join('pyutilkit', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break
    else:
        version = '0.1.0'

setup(
    name="pyutilkit-sarvs",
    version="0.1.0",
    description='A multi-purpose Python utility toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sarvesh Kannan',
    author_email='your.email@example.com',  # Replace with your email
    url='https://github.com/Sarvesh-Kannan/PyUtilKit',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    keywords='utility, helper, tools, string manipulation, file handling, mathematics',
    project_urls={
        'Bug Reports': 'https://github.com/Sarvesh-Kannan/PyUtilKit/issues',
        'Source': 'https://github.com/Sarvesh-Kannan/PyUtilKit',
    },
) 
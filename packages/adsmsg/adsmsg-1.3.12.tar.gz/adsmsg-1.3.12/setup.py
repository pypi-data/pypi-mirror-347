#!/usr/bin/env python
"""
ADSPipelineMsg
-------------
Interpipeline communication messages
"""
import os
import re
from subprocess import Popen, PIPE

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('dev-requirements.txt') as f:
    dev_required = f.read().splitlines()

def get_git_version(default="0.0.1"):
    """
    Get version from git tags, but clean it to be PEP 440 compliant.
    Format: Remove leading 'v', convert git describe post-commit info to .devN format
    Example: 'v1.3.11-4-g7ce3f79' becomes '1.3.11.dev4+g7ce3f79'
    """
    try:
        p = Popen(['git', 'describe', '--tags'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        line = line.strip().decode()
        
        # If exact tag match, remove v prefix if present and return
        if '-' not in line:
            return line[1:] if line.startswith('v') else line
        
        # For versions with commits after tag, convert to PEP 440 dev format
        # Example: v1.3.11-4-g7ce3f79 → 1.3.11.dev4+g7ce3f79
        version_match = re.match(r'v?([0-9]+\.[0-9]+\.[0-9]+)-([0-9]+)-g([0-9a-f]+)', line)
        if version_match:
            version, commits, hash = version_match.groups()
            return f"{version}.dev{commits}+g{hash}"
        
        # Fallback - strip v prefix and return as is
        return line[1:] if line.startswith('v') else line
    except:
        return default

setup(
    name='adsmsg',
    version=get_git_version(default="v0.0.1"),
    url='http://github.com/adsabs/flask-discoverer/',
    license='MIT',
    author='NASA/SAO ADS',
    description='Interpipeline communication messages',
    long_description=__doc__,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=required,
    test_suite='adsmsg/tests',
    tests_require = dev_required,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

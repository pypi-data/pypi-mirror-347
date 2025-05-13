"""
Setup file for vapi client bindings
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2012-2022 VMware, Inc.  All rights reserved. -- VMware Confidential'

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
from com.vmware.vapi import __version__

setup(
    name = 'oab_vcenter_bindings',
    url = 'https://github.com/vmware/vsphere-automation-sdk-python',
    version = "4.2.0",
    author= 'VMware, Inc.',
    keywords='VMware',
    description = 'VMware vCenter vAPI Client Bindings',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Distributed Computing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    packages = find_packages(),
    license_files = ['LICENSE'],
    license='License :: OSI Approved :: MIT License',
    install_requires = [
        'setuptools',
        'oab_vapi_runtime>=2.9.0',
    ]
)
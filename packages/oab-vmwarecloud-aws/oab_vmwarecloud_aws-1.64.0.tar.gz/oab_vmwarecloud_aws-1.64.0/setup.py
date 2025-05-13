"""
Setup file for vmc client bindings
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2018, 2023 VMware, Inc.  All rights reserved. -- VMware Confidential'

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='oab_vmwarecloud_aws',
    version='1.64.0',
    author = 'VMware, Inc.',
    url='https://github.com/vmware/vsphere-automation-sdk-python/tree/master/lib/src/vmwarecloud-aws',
    keywords='VMware',
    description='Client bindings for VMware Cloud on AWS',
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
    packages=find_packages(),
    license_files = ['LICENSE'],
    license='License :: OSI Approved :: MIT License',
    install_requires=[
        'setuptools',
        'oab_vapi_common_client',
        'oab_vapi_runtime',
    ]
)
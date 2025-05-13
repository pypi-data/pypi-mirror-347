"""
Setup file for vAPI Common Client package
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2017, 2023 VMware, Inc.  All rights reserved. -- VMware Confidential'


from setuptools import setup, find_packages
setup(
    name='vapi_common_client',
    version='2.44.0',
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
    description='vAPI Common Services Client Bindings',
    url='https://github.com/vmware/vsphere-automation-sdk-python/tree/master/lib/src/vapi-common-client',
    license_files='LICENSE.txt',
    license='License :: OSI Approved :: MIT License',
    install_requires=['vapi-runtime==2.44.0'],
    author='VMware, Inc.',
    keywords='VMware',
)

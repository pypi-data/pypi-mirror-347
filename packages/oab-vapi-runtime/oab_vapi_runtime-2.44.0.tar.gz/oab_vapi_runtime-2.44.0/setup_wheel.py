"""
Setup file for creating Runtime package
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2017-2019, 2022-2023 VMware, Inc.  All rights reserved. -- VMware Confidential'  # pylint: disable=line-too-long

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages  # pylint: disable=ungrouped-imports

import os

setup(
    name='vapi_runtime',
    version='2.44.0',
    description='vAPI Runtime',
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
    keywords='VMware',
    author='VMware, Inc.',
    url='https://github.com/vmware/vsphere-automation-sdk-python/tree/master/lib/src/vapi-runtime',
    data_files=[('', ['requirements.txt'])],
    license_files='LICENSE.txt',
    license='License :: OSI Approved :: MIT License',
    packages=find_packages(),
    package_data={
        'vmware': ['vapi/settings/*.properties'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyOpenSSL',
                      'requests>=2.0.0,<3.0.0',
                      'six>=1.0.0,<2.0.0'],
    extras_require={
        'twisted': ['twisted>=18.0.0', 'service_identity>=18.0.0',
                    'lxml>=4.3.0', 'werkzeug>=0.14.1', 'urllib3>=1.25.1'],
        'server': ['lxml>=4.3.0', 'werkzeug>=0.14.1', 'urllib3>=1.25.1'],
    },
    entry_points={
        'console_scripts': [
            'vapi-server = vmware.vapi.server.vapid:main'
        ]
    }
)

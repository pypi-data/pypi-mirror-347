"""
Setup file for creating Runtime package
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2015, 2017-2020, 2022 VMware, Inc.  All rights reserved. -- VMware Confidential'  # pylint: disable=line-too-long

import os

from egg_utils import get_command_options_for_custom_egg_name  # pylint: disable=import-error

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages  # pylint: disable=ungrouped-imports

name = 'uc_vapi_runtime'

version = '2.44.1'

setup(
    name=name,
    version=version,
    description='vAPI Runtime',
    classifiers=[],
    keywords='VMware',
    author='VMware',
    namespace_packages=['vmware'],
    data_files=[('', ['requirements.txt'])],
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
    },
    command_options=get_command_options_for_custom_egg_name(name, version)
)

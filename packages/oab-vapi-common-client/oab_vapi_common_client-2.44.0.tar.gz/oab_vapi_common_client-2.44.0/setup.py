"""
Setup file for vAPI Common Client package
"""
__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2012-2014, 2020 VMware, Inc.  All rights reserved. -- VMware Confidential'


from setuptools import setup, find_packages

from egg_utils import get_command_options_for_custom_egg_name  # pylint: disable=import-error

name = 'oab_vapi_common_client'

version = '2.44.0'

setup(
    name=name,
    version=version,
    namespace_packages=['com'],
    packages=find_packages(),
    description='vAPI Common Services Client Bindings',
    install_requires=['oab_vapi-runtime==2.44.0'],
    author='VMware',
    command_options=get_command_options_for_custom_egg_name(name, version)
)

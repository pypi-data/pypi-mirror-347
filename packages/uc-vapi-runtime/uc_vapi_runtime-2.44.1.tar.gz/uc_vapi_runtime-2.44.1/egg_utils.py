"""
Utilities for Egg packaging
"""
__author__ = "VMware, Inc."
__copyright__ = "Copyright 2020 VMware, Inc.  All rights reserved. -- VMware Confidential"


def get_command_options_for_custom_egg_name(package_name, package_version):
    """Command options are used so we can have a custom names for the egg:
    {package-name}-{package-version}.egg

    The default egg name looks like this:
    {package-name}-{package-version}-{python-version}.egg
    Where {python-version} is the version of python used to package the egg.
    This gives no useful information and anyone who consumes the egg might
    have to change it whenever we bump the python used to package the egg.
    """
    egg_name = "dist/{0}-{1}.egg".format(package_name, package_version)

    return {"bdist_egg": {"egg_output": ("_", egg_name)}}

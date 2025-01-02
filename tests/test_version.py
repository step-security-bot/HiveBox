"""Module testing the application version module."""

from ..src.endpoints import version

def test_list_version():
    """ Test that the module returns the expected version number"""
    version_number = "0.0.8"
    assert version.list_version() == version_number

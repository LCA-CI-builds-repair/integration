"""HACS configuration schema Test Suite."""
# pylint: disable=missing-docstring
from custom_components.hacs.utils.configuration_schema import hacs_config_combined


def test_combined():
    """Test the hacs_config_combined function."""
    assert isinstance(hacs_config_combined(), dict)
"""Example tests demonstrating different markers."""

import time

import pytest

from iptag.settings import IptagSettings


@pytest.mark.unit
def test_settings_initialization():
    """Test that settings can be initialized - marked as unit test."""
    settings = IptagSettings()
    assert settings is not None


@pytest.mark.unit
def test_example_function():
    """Example unit test function."""
    assert 1 + 1 == 2


@pytest.mark.integration
def test_settings_integration():
    """Example integration test for settings."""
    settings = IptagSettings(debug=True)
    # This would test integration between components
    assert settings.debug is True


@pytest.mark.slow
def test_slow_operation():
    """Example slow test that takes time to run."""
    time.sleep(2)  # Simulate a slow operation
    assert True


@pytest.mark.slow
@pytest.mark.integration
def test_slow_integration():
    """Example test with multiple markers."""
    time.sleep(1)
    settings = IptagSettings()
    assert isinstance(settings, IptagSettings)


class TestExampleClass:
    """Example test class."""

    @pytest.mark.unit
    def test_method_example(self):
        """Example unit test method."""
        assert "hello".upper() == "HELLO"

    @pytest.mark.integration
    def test_method_integration(self):
        """Example integration test method."""
        data = {"key": "value"}
        assert data["key"] == "value"

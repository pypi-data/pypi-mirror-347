import pytest

def pytest_configure(config):
    """Configure pytest."""
    # Define fixture loop scope to avoid warnings
    config.option.asyncio_fixture_loop_scope = "function"

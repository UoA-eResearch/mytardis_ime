"""
conftest.py contains code common to all
tests. See https://docs.pytest.org/en/7.1.x/reference/fixtures.html
"""
from ime.models import IngestionMetadata
import pytest


@pytest.fixture
def metadata(request):
    # This path is relative to where pytest is run.
    # So run pytest at the root directory.
    return IngestionMetadata.from_file('ime/tests/fixtures.yaml')

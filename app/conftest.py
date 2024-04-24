# conftest.py
import pytest
from app.adapters import DatabaseAdapter


@pytest.fixture
def db_adapter():
    return DatabaseAdapter(db_url="sqlite:///:memory:")

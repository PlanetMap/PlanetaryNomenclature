import pytest
from nomen import create_app

TestApp = create_app('Test')

@pytest.fixture
def active_context():
    active_context = TestApp.app_context()
    yield active_context

@pytest.fixture
def active_client():
    active_client = TestApp.test_client()
    yield active_client
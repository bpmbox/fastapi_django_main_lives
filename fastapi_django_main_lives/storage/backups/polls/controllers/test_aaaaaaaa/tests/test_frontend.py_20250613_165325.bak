import pytest
from frontend.app import app

@pytest.fixture
def interface():
    return app

def test_user_list(interface):
    assert interface.get_component("user_list") is not None

def test_user_detail(interface):
    assert interface.get_component("user_detail") is not None

def test_team_list(interface):
    assert interface.get_component("team_list") is not None
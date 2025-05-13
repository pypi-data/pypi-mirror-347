import pytest

from patronus._api import API


@pytest.fixture()
def api_client():
    return API()


@pytest.fixture()
def client(): ...

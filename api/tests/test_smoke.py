import pytest
import requests
from pytest_socket import SocketBlockedError


def test_no_network_requests():
    with pytest.raises(SocketBlockedError):
        requests.get("https://example.com/")

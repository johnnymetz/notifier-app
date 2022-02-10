import sys
from unittest import mock

import pytest
from gunicorn.app.wsgiapp import run


def test_gunicorn_config():
    argv = [
        "gunicorn",
        "--check-config",
        "--config",
        "python:api.gunicorn_conf",
        "api.wsgi",
    ]
    mock_argv = mock.patch.object(sys, "argv", argv)

    with pytest.raises(SystemExit) as e, mock_argv:
        run()

    assert e.value.args[0] == 0

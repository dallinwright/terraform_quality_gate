import json
from contextlib import contextmanager
from unittest.mock import patch, MagicMock

import pytest

from modules.call_os_command import status_check
from modules.terratest.terratest_terraform_cloud import write_token


@contextmanager
def not_raises(ExpectedException):
    try:
        yield

    except ExpectedException as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


def test_status_check():
    """
    Verify status code check does a sys exit, or not
    :return:
    """
    with pytest.raises(SystemExit):
        status_check(1)

    with pytest.raises(SystemExit):
        status_check(100)

    with not_raises(ValueError):
        status_check(0)


def test_write_token(tmpdir):
    """
    Test function opens and writes a a file
    :return:
    """
    expected_content = json.dumps({
        "credentials": {
            "app.terraform.io": {
                "token": "test_token"
            }
        }
    })

    m = MagicMock(side_effect=[expected_content])
    open_mock = m.mock_open()
    filename = "output.json"

    # Test function is called, and file write is called with the following args
    # This successfully example_terratests the open functionality in the main function

    with patch("builtins.open", open_mock, create=True):
        write_token(filename, "test_token")
        open_mock.assert_called_with('output.json', 'w', encoding='utf-8')

        patch_two = patch("json.load", m)

        with patch_two as p_json_load:
            f = open(filename)
            content_json = json.load(f)
            content_string = json.dumps(content_json)
            expected_content_string = json.dumps(expected_content)
            print(content_string)
            print(expected_content_string)
            assert content_string == expected_content_string

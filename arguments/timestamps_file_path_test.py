from unittest.mock import patch
from arguments.timestamps_file_path import validate


@patch("utils.file.verify_mime_type", return_value=True)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_text_file_exists(
    mocked_file_path_exists, mocked_verify_mime_type
):
    assert validate("text.txt")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=False)
def test_validate_when_text_file_does_not_exist(
    mocked_file_path_exists, mocked_verify_mime_type
):
    assert not validate("text.txt")
    assert mocked_file_path_exists.called
    assert not mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_file_exists_but_its_not_text(
    mocked_file_path_exists, mocked_verify_mime_type
):
    assert not validate("text.txt")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called

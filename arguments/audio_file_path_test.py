from unittest.mock import patch
from arguments.audio_file_path import validate


@patch("utils.file.verify_mime_type", return_value=True)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_audio_file_exists(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file exists and it is an audio file
    """

    assert validate("audio.mp3")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=False)
def test_validate_when_audio_file_does_not_exist(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file does not exist and it doesn't validate
    its mime type after determining it is not an existing file
    """

    assert not validate("audio.mp3")
    assert mocked_file_path_exists.called
    assert not mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_file_exists_but_its_not_audio(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file exists and it is not an audio file
    """

    assert not validate("audio.mp3")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called

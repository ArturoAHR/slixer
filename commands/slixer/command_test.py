import pytest
import argparse
from unittest.mock import patch
from commands.slixer.command import slixer


@pytest.fixture
def mock_audio_file_path_validate():
    with patch("arguments.audio_file_path.validate") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_timestamps_file_path_validate():
    with patch("arguments.timestamps_file_path.validate") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_timestamps_file_path_extract_timestamps():
    with patch("arguments.timestamps_file_path.extract_timestamps") as mock:
        mock.return_value = []
        yield mock


@pytest.fixture
def mock_slixer_utils_split_audio_file():
    with patch("commands.slixer.command.split_audio_file") as mock:
        yield mock


def test_slixer(
    mock_audio_file_path_validate,
    mock_timestamps_file_path_validate,
    mock_timestamps_file_path_extract_timestamps,
    mock_slixer_utils_split_audio_file,
):
    args = argparse.Namespace()
    args.audio_file_path = "/path/to/audio.mp3"
    args.timestamps_file_path = "/path/to/timestamps.txt"

    slixer(args)

    assert mock_audio_file_path_validate.called
    assert mock_timestamps_file_path_validate.called
    assert mock_timestamps_file_path_extract_timestamps.called
    assert mock_slixer_utils_split_audio_file.called


def test_slixer_when_audio_file_is_invalid(
    mock_audio_file_path_validate,
):
    mock_audio_file_path_validate.return_value = False

    args = argparse.Namespace()
    args.audio_file_path = "/path/to/audio.mp3"
    args.timestamps_file_path = "/path/to/timestamps.txt"

    with pytest.raises(FileNotFoundError) as context:
        slixer(args)

    assert "Audio file not found" in str(context.value)


def test_slixer_when_timestamps_file_is_invalid(
    mock_audio_file_path_validate,
    mock_timestamps_file_path_validate,
):
    mock_timestamps_file_path_validate.return_value = False

    args = argparse.Namespace()
    args.audio_file_path = "/path/to/audio.mp3"
    args.timestamps_file_path = "/path/to/timestamps.txt"

    with pytest.raises(FileNotFoundError) as context:
        slixer(args)

    assert "Timestamps file not found" in str(context.value)

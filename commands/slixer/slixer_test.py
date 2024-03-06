import pytest
import argparse
from unittest.mock import patch
from commands.slixer.slixer import slixer


@pytest.fixture
def default_args():
    return argparse.Namespace(
        audio_file_path="audio.mp3",
        timestamps_file_path="timestamps.txt",
        preview=False,
    )


@pytest.fixture
def mock_audio_file_path_validate():
    with patch("arguments.audio_file_path.audio_file_path.validate") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_timestamps_file_path_validate():
    with patch(
        "arguments.timestamps_file_path.timestamps_file_path.validate"
    ) as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_timestamps_file_path_extract_timestamps():
    with patch(
        "arguments.timestamps_file_path.timestamps_file_path.extract_timestamps"  # noqa: E501
    ) as mock:
        mock.return_value = []
        yield mock


@pytest.fixture
def mock_slixer_utils_split_audio_file():
    with patch("commands.slixer.slixer.split_audio_file") as mock:
        yield mock


@pytest.fixture
def mock_slixer_utils_preview_slixer_output():
    with patch("commands.slixer.slixer.preview_slixer_output") as mock:
        yield mock


def test_slixer(
    default_args,
    mock_audio_file_path_validate,
    mock_timestamps_file_path_validate,
    mock_timestamps_file_path_extract_timestamps,
    mock_slixer_utils_split_audio_file,
):
    """
    Correctly calls all necessary validations and audio splitting functions
    """

    slixer(default_args)

    assert mock_audio_file_path_validate.called
    assert mock_timestamps_file_path_validate.called
    assert mock_timestamps_file_path_extract_timestamps.called
    assert mock_slixer_utils_split_audio_file.called


def test_slixer_when_audio_file_is_invalid(
    default_args,
    mock_audio_file_path_validate,
):
    """
    Correctly raises an error when the given audio file does not pass
    validations
    """

    mock_audio_file_path_validate.return_value = False

    with pytest.raises(FileNotFoundError) as context:
        slixer(default_args)

    assert "Audio file not found" in str(context.value)


def test_slixer_when_timestamps_file_is_invalid(
    default_args,
    mock_audio_file_path_validate,
    mock_timestamps_file_path_validate,
):
    """
    Correctly raises an error when the given timestamps file does not pass
    validations
    """

    mock_timestamps_file_path_validate.return_value = False

    with pytest.raises(FileNotFoundError) as context:
        slixer(default_args)

    assert "Timestamps file not found" in str(context.value)


def test_slixer_when_preview_must_be_shown(
    default_args,
    mock_audio_file_path_validate,
    mock_timestamps_file_path_validate,
    mock_timestamps_file_path_extract_timestamps,
    mock_slixer_utils_split_audio_file,
    mock_slixer_utils_preview_slixer_output,
):
    """
    Correctly calls the preview output function when the preview argument is
    used
    """

    mocked_timestamps = [
        {
            "start_time": (0, 0, 0),
            "segment_title": "Segment 1",
        },
        {
            "start_time": (0, 0, 10),
            "segment_title": "Segment 2",
        },
    ]

    mock_timestamps_file_path_extract_timestamps.return_value = (
        mocked_timestamps
    )

    default_args.preview = True

    slixer(default_args)

    assert mock_slixer_utils_preview_slixer_output.called
    mock_slixer_utils_preview_slixer_output.assert_called_once_with(
        mocked_timestamps
    )

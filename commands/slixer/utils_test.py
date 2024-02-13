import pytest
from unittest.mock import patch, ANY, MagicMock
from commands.slixer.utils import split_audio_file


@pytest.fixture
def mock_audio_segment():
    with patch("pydub.AudioSegment.from_file") as mock:
        mock.return_value = MagicMock()
        mock.return_value.__len__.return_value = 120000
        yield mock


@patch("utils.file.export_audio_file")
def test_audio_file_splitting(mock_export_audio_file, mock_audio_segment):
    audio_file_path = "path/fake/audio.mp3"
    timestamps = [
        {"start_time": (0, 0, 0), "segment_title": "Intro"},
        {"start_time": (0, 1, 0), "segment_title": "Verse"},
    ]

    split_audio_file(audio_file_path, timestamps)

    mock_audio_segment.assert_called_with(audio_file_path)
    assert mock_export_audio_file.call_count == len(timestamps)

    for timestamp in timestamps:
        format = "mp3"
        expected_title = timestamp["segment_title"]
        mock_export_audio_file.assert_any_call(ANY, expected_title, format)


@patch("utils.file.export_audio_file")
def test_audio_file_splitting_when_timestamp_exceeds_audio_length(
    mock_export_audio_file,
    mock_audio_segment,
):
    audio_file_path = "path/fake/audio.mp3"
    timestamps = [
        {"start_time": (0, 0, 0), "segment_title": "Intro"},
        {"start_time": (0, 1, 0), "segment_title": "Verse"},
        {"start_time": (0, 3, 0), "segment_title": "Beyond audio length"},
    ]

    with pytest.raises(ValueError) as context:
        split_audio_file(audio_file_path, timestamps)

    assert (
        "Start time for Timestamp Beyond audio length exceeds audio length"
        in str(context.value)
    )

    mock_audio_segment.assert_called_with(audio_file_path)
    assert mock_export_audio_file.call_count == 2

    for timestamp in timestamps[:2]:
        format = "mp3"
        expected_title = timestamp["segment_title"]
        mock_export_audio_file.assert_any_call(ANY, expected_title, format)


@patch("utils.file.export_audio_file")
def test_audio_file_splitting_when_file_format_is_not_supported(
    mock_audio_segment,
):
    audio_file_path = "path/fake/audio.txt"
    timestamps = [
        {"start_time": (0, 0, 0), "segment_title": "Intro"},
        {"start_time": (0, 1, 0), "segment_title": "Verse"},
    ]

    with pytest.raises(ValueError) as context:
        split_audio_file(audio_file_path, timestamps)

    assert "Unsupported file format: txt" in str(context.value)
    mock_audio_segment.assert_not_called()


@patch("utils.file.export_audio_file")
def test_audio_file_splitting_when_there_are_invalid_file_characters(
    mock_export_audio_file, mock_audio_segment
):
    audio_file_path = "path/fake/audio.mp3"
    timestamps = [
        {
            "start_time": (0, 0, 0),
            "segment_title": 'Invalid title one \\/"*?<>|',
        },
        {
            "start_time": (0, 1, 0),
            "segment_title": '\\/"*?<>| Invalid title two',
        },
    ]

    expected_titles = [
        "Invalid title one ________",
        "________ Invalid title two",
    ]

    split_audio_file(audio_file_path, timestamps)

    mock_audio_segment.assert_called_with(audio_file_path)
    assert mock_export_audio_file.call_count == len(timestamps)

    for expected_title in expected_titles:
        format = "mp3"
        mock_export_audio_file.assert_any_call(ANY, expected_title, format)

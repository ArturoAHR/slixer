import pytest
from unittest.mock import patch, ANY
from commands.slixer.utils import split_audio_file


@pytest.fixture
def mock_audio_segment(mocker):
    mock_audio = mocker.MagicMock()
    mocker.patch("pydub.AudioSegment.from_file", return_value=mock_audio)
    mock_audio.__len__.return_value = 120000
    return mock_audio


@patch("utils.file.export_audio_file")
def test_audio_file_splitting(mock_export_audio_file, mock_audio_segment):
    audio_file_path = "path/fake/audio.mp3"
    timestamps = [
        {"start_time": (0, 0, 0), "song_title": "Intro"},
        {"start_time": (0, 1, 0), "song_title": "Verse"},
    ]

    split_audio_file(audio_file_path, timestamps)

    assert mock_audio_segment.from_file.called_with(audio_file_path)
    assert mock_export_audio_file.call_count == len(timestamps)

    for timestamp in timestamps:
        format = "mp3"
        expected_title = timestamp["song_title"]
        mock_export_audio_file.assert_any_call(ANY, expected_title, format)


@patch("utils.file.export_audio_file")
def test_audio_file_splitting_when_file_format_is_not_supported(
    mock_export_audio_file, mock_audio_segment
):
    audio_file_path = "path/fake/audio.txt"
    timestamps = [
        {"start_time": (0, 0, 0), "song_title": "Intro"},
        {"start_time": (0, 1, 0), "song_title": "Verse"},
    ]

    with pytest.raises(ValueError) as context:
        split_audio_file(audio_file_path, timestamps)

    assert "Unsupported file format: txt" in str(context.value)
    mock_audio_segment.from_file.assert_not_called()

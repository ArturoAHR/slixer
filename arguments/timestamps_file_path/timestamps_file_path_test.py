from unittest.mock import mock_open, patch
from arguments.timestamps_file_path.timestamps_file_path import (
    validate,
    extract_timestamps,
)


@patch("utils.file.verify_mime_type", return_value=True)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_text_file_exists(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file exists and it is a text file
    """

    assert validate("text.txt")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=False)
def test_validate_when_text_file_does_not_exist(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file does not exist and it doesn't validate
    its mime type after determining it is not an existing file
    """

    assert not validate("text.txt")
    assert mocked_file_path_exists.called
    assert not mocked_verify_mime_type.called


@patch("utils.file.verify_mime_type", return_value=False)
@patch("utils.file.file_path_exists", return_value=True)
def test_validate_when_file_exists_but_its_not_text(
    mocked_file_path_exists, mocked_verify_mime_type
):
    """
    Validates correctly when the file exists and it is not a text file
    """

    assert not validate("text.txt")
    assert mocked_file_path_exists.called
    assert mocked_verify_mime_type.called


def test_timestamp_extraction():
    """
    Extracts timestamps correctly with the hh:mm:ss format for segment start
    time
    """

    mocked_timestamps_file_contents = """00:00:00 Segment 1
00:03:00 Segment 2
00:06:00 Segment 3
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert (
            timestamps == expected_timestamps
        ), "Timestamps should have been extracted"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_segment_time_is_shortened():
    """
    Extracts timestamps correctly with the mm:ss format for segment start time
    """

    mocked_timestamps_file_contents = """00:00 Segment 1
03:00 Segment 2
06:00 Segment 3
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert (
            timestamps == expected_timestamps
        ), "Timestamps should have been extracted"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_are_unsorted():
    """
    Extracts timestamps sorting them out by start time
    """

    mocked_timestamps_file_contents = """00:00:00 Segment 1
00:06:00 Segment 3
00:03:00 Segment 2
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert (
            timestamps == expected_timestamps
        ), "Timestamps should be sorted by start time"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_titles_are_missing():
    """
    Extracts timestamps filling out missing titles with 'Untitled Segment
    {index}'
    """

    mocked_timestamps_file_contents = """00:00:00 Segment 1
00:03:00 Segment 2
00:06:00
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Untitled Segment 3"},
        ]

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_have_time_between_characters():
    """
    Extracts timestamps correctly when the time is surrounded by characters
    """

    mocked_timestamps_file_contents = """(00:00:00) Segment 1
[00:03:00] Segment 2
/00:06:00/ Segment 3
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert timestamps == expected_timestamps
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_dash_characters():
    """
    Extracts timestamps correctly when the time and the segment title are
    separated by a dash and the time is surrounded by characters
    """

    mocked_timestamps_file_contents = """(00:00:00) - Segment 1
[00:03:00] - Segment 2
/00:06:00/ - Segment 3
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert timestamps == expected_timestamps
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_have_time_at_the_end():
    """
    Extracts timestamps correctly when the time is at the end of the line
    """

    mocked_timestamps_file_contents = """Segment 1 00:00:00
Segment 2 00:03:00
Segment 3 00:06:00
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert timestamps == expected_timestamps
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_between_characters_end():
    """
    Extracts timestamps correctly when the time is at the end surrounded by
    characters
    """

    mocked_timestamps_file_contents = """Segment 1 (00:00:00)
Segment 2 [00:03:00]
Segment 3 /00:06:00/
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert timestamps == expected_timestamps
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_dash_characters_end():
    """
    Extracts timestamps correctly when the time and the segment title are
    separated by a dash and the time is at the end surrounded by characters
    """

    mocked_timestamps_file_contents = """Segment 1 - (00:00:00)
Segment 2 - [00:03:00]
Segment 3 - /00:06:00/
"""

    with patch(
        "builtins.open", mock_open(read_data=mocked_timestamps_file_contents)
    ) as mocked_open:
        timestamps = extract_timestamps("/fake/path/timestamps.txt")

        expected_timestamps = [
            {"start_time": (0, 0, 0), "segment_title": "Segment 1"},
            {"start_time": (0, 3, 0), "segment_title": "Segment 2"},
            {"start_time": (0, 6, 0), "segment_title": "Segment 3"},
        ]

        assert timestamps == expected_timestamps
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")

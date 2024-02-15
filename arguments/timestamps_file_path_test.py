from unittest.mock import mock_open, patch
from arguments.timestamps_file_path import validate, extract_timestamps


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


def test_timestamp_extraction():
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

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_dash_characters():
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

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_have_time_at_the_end():
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

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_between_characters_end():
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

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")


def test_timestamp_extraction_when_timestamps_time_dash_characters_end():
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

        assert (
            timestamps == expected_timestamps
        ), "Missing titles should be replaced with 'Untitled Segment {index}'"
        mocked_open.assert_called_with("/fake/path/timestamps.txt", "r")

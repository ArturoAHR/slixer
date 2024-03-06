import pytest
from unittest.mock import patch
from commands.slixer.utils.preview_slixer_output import preview_slixer_output


@pytest.fixture
def default_timestamps():
    return [
        {
            "start_time": (0, 0, 0),
            "segment_title": "Segment 1",
        },
        {
            "start_time": (0, 0, 10),
            "segment_title": "Segment 2",
        },
    ]


@pytest.fixture
def mock_builtins_print():
    with patch("builtins.print") as mock:
        yield mock


@pytest.fixture
def mock_builtins_exit():
    with patch("builtins.exit") as mock:
        yield mock


def test_preview_slixer_output(
    default_timestamps,
    mock_builtins_print,
):
    """
    Correctly showcases preview of segments based on the timestamps passed in
    """

    with patch("builtins.input", side_effect=["y"]) as mock_builtins_input:
        preview_slixer_output(default_timestamps)

        expected_calls = [
            "Output Preview: ",
            "(1/2) 00:00:00 - Segment 1",
            "(2/2) 00:00:10 - Segment 2",
            "\nDo you wish to proceed? (y/n)\n",
        ]

        for expected_call in expected_calls:
            mock_builtins_print.assert_any_call(expected_call)
        assert mock_builtins_input.call_count == 1


def test_preview_slixer_output_when_user_does_not_proceed(
    default_timestamps, mock_builtins_print, mock_builtins_exit
):
    """
    Correctly stops execution when user does not wish to proceed
    """

    with patch("builtins.input", side_effect=["n"]) as mock_builtins_input:
        preview_slixer_output(default_timestamps)

        expected_calls = [
            "Output Preview: ",
            "(1/2) 00:00:00 - Segment 1",
            "(2/2) 00:00:10 - Segment 2",
            "\nDo you wish to proceed? (y/n)\n",
            "Aborting...",
        ]

        for expected_call in expected_calls:
            mock_builtins_print.assert_any_call(expected_call)
        assert mock_builtins_input.call_count == 1
        assert mock_builtins_exit.called


def test_preview_slixer_output_when_confirmation_input_is_invalid(
    default_timestamps,
    mock_builtins_print,
):
    """
    Correctly retries y/n prompt when an invalid input is given
    """

    with patch(
        "builtins.input", side_effect=["invalid", "y"]
    ) as mock_builtins_input:
        preview_slixer_output(default_timestamps)

        expected_calls = [
            "Output Preview: ",
            "(1/2) 00:00:00 - Segment 1",
            "(2/2) 00:00:10 - Segment 2",
            "\nDo you wish to proceed? (y/n)\n",
            "Invalid input. Please enter 'y' or 'n'.",
        ]

        for expected_call in expected_calls:
            mock_builtins_print.assert_any_call(expected_call)
        assert mock_builtins_input.call_count == 2

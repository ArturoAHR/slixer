from unittest.mock import patch
from main import main


@patch("main.slixer")
def test_slixer_command(mock_slixer):
    test_args = [
        "slixer",
        "/path/to/audio.mp3",
        "-t",
        "/path/to/timestamps.txt",
    ]
    with patch("sys.argv", test_args):
        main()

        assert mock_slixer.called

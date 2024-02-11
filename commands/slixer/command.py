import argparse
from arguments import audio_file_path
from arguments import timestamps_file_path
from commands.slixer.utils import split_audio_file


def slixer(args: argparse.Namespace):
    if not audio_file_path.validate(args.audio_file_path):
        raise FileNotFoundError("Audio file not found")

    if not timestamps_file_path.validate(args.timestamps_file_path):
        raise FileNotFoundError("Timestamps file not found")

    timestamps = timestamps_file_path.extract_timestamps(
        args.timestamps_file_path
    )

    split_audio_file(args.audio_file_path, timestamps)

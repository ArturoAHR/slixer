from pydub import AudioSegment
from utils import time, file


def split_audio_file(audio_file_path: str, timestamps: list):
    print(f"Loading {audio_file_path}")

    format = file.get_file_extension(audio_file_path)

    if not file.is_file_format_supported(format):
        raise ValueError(f"Unsupported file format: {format}")

    audio = AudioSegment.from_file(audio_file_path)

    for index in range(len(timestamps)):
        timestamp = timestamps[index]
        next_timestamp = (
            timestamps[index + 1] if index + 1 < len(timestamps) else None
        )

        print(
            f"({index + 1}/{len(timestamps)}) "
            f"Slicing \"{timestamp['song_title']}\""
        )

        next_timestamp_start_time_ms = len(audio)

        if next_timestamp is not None:
            next_timestamp_start_time_ms = time.convert_to_ms(
                next_timestamp["start_time"]
            )

        start_time = time.convert_to_ms(timestamp["start_time"])
        end_time = min(len(audio), next_timestamp_start_time_ms)

        if start_time > len(audio):
            raise ValueError(
                f"Start time for Timestamp {timestamp['song_title']}"
                " exceeds audio length"
            )

        audio_segment = audio[start_time:end_time]

        file.export_audio_file(audio_segment, timestamp["song_title"], format)

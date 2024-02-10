from pydub import AudioSegment
from utils import time


def split_audio_file(audio_file_path: str, timestamps: list):
    print(f"Loading {audio_file_path}")

    audio = AudioSegment.from_file(audio_file_path)

    for index in range(len(timestamps)):

        timestamp = timestamps[index]
        next_timestamp = (
            timestamps[index + 1] if index + 1 < len(timestamps) else None
        )

        next_timestamp_start_time_ms = time.convert_to_ms(
            next_timestamp["start_time"]
        )

        print(
            f"({index + 1}/{len(timestamps)}) "
            f"Slicing \"{timestamp['song_title']}\""
        )

        start_time = time.convert_to_ms(timestamp["start_time"])
        end_time = (
            len(audio)
            if next_timestamp is None
            or next_timestamp_start_time_ms >= len(audio)
            else next_timestamp_start_time_ms
        )

        if start_time > len(audio):
            raise ValueError(
                f"Start time for Timestamp {timestamp['song_title']}"
                " exceeds audio length"
            )

        audio_segment = audio[start_time:end_time]
        audio_segment.export(f"{timestamp['song_title']}.mp3", format="mp3")

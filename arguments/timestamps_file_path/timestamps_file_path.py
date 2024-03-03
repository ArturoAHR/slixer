from utils import file, time
from arguments.timestamps_file_path.utils.extract_timestamp_start_time import (
    extract_timestamp_start_time,
)


def validate(timestamps_file_path: str) -> bool:
    return file.file_path_exists(
        timestamps_file_path
    ) and file.verify_mime_type(timestamps_file_path, prefix="text/")


def extract_timestamps(timestamps_file_path: str) -> list:
    timestamps = []

    with open(timestamps_file_path, "r") as file:
        lines = file.readlines()

        for index, line in enumerate(lines):
            timestamp_parts = line.split(" ", 1)

            segment_title = f"Untitled Segment {index + 1}"

            if len(timestamp_parts) > 1:
                segment_title = timestamp_parts[1].strip()

            start_time = extract_timestamp_start_time(line)

            timestamps.append(
                {
                    "start_time": start_time,
                    "segment_title": segment_title,
                }
            )

    timestamps.sort(key=lambda x: time.convert_to_ms(x["start_time"]))

    return timestamps

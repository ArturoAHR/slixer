from utils import file, time


def validate(timestamps_file_path: str) -> bool:
    return file.file_path_exists(
        timestamps_file_path
    ) and file.verify_mime_type(timestamps_file_path, prefix="text/")


def extract_timestamps(timestamps_flle_path: str) -> list:
    timestamps = []

    with open(timestamps_flle_path, "r") as file:
        lines = file.readlines()

        for index, line in enumerate(lines):
            timestamp_parts = line.split(" ", 1)

            timestamp = timestamp_parts[0]
            song_title = f"Untitled Song {index + 1}"

            if len(timestamp_parts) > 1:
                song_title = timestamp_parts[1].strip()

            timestamp_splitted = timestamp.split(":")

            hours = 0
            minutes = int(timestamp_splitted[0])
            seconds = int(timestamp_splitted[1])

            if len(timestamp_splitted) == 3:
                hours = int(timestamp_splitted[0])
                minutes = int(timestamp_splitted[1])
                seconds = int(timestamp_splitted[2])

            timestamps.append(
                {
                    "timestamp": (hours, minutes, seconds),
                    "song_title": song_title,
                }
            )

    timestamps.sort(key=lambda x: time.convert_to_ms(x["timestamp"]))

    return timestamps

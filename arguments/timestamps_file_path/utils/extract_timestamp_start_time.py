import re


def extract_timestamp_start_time(timestamp: str) -> tuple[int, int, int]:
    start_time_extraction_pattern = r"(\d*:?\d+:\d{2})"

    start_time = re.search(start_time_extraction_pattern, timestamp).group(0)

    timestamp_splitted = start_time.split(":")

    hours = 0
    minutes = int(timestamp_splitted[0])
    seconds = int(timestamp_splitted[1])

    if len(timestamp_splitted) == 3:
        hours = int(timestamp_splitted[0])
        minutes = int(timestamp_splitted[1])
        seconds = int(timestamp_splitted[2])

    return (hours, minutes, seconds)

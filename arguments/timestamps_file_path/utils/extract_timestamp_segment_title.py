import re


def extract_timestamp_segment_title(timestamp: str) -> str:
    timestamp_extraction_pattern = r"(-\s)?\S?(\d*:?\d+:\d{2})\S?(\s-)?"

    segment_title = re.sub(timestamp_extraction_pattern, "", timestamp).strip()

    return segment_title

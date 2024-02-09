from utils import file


def validate(timestamps_file_path: str) -> bool:
    return file.file_path_exists(
        timestamps_file_path
    ) and file.verify_mime_type(timestamps_file_path, prefix="text/")

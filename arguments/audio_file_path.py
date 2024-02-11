from utils import file


def validate(audio_file_path: str) -> bool:
    return file.file_path_exists(audio_file_path) and file.verify_mime_type(
        audio_file_path, prefix="audio/"
    )

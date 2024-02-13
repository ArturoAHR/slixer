import os
import mimetypes
from pydub import AudioSegment

invalid_file_name_characters = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
supported_file_formats = [
    "mp3",
    "wav",
    "aac",
    "ogg",
    "flac",
    "opus",
    "m4a",
    "alac",
    "wma",
    "mp4",
    "aiff",
    "mka",
    "mkv",
    "webm",
    "mov",
    "avi",
]


def file_path_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def verify_mime_type(
    file_path: str, prefix: str = "default", suffix: str = "default"
) -> bool:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mimetypes is not None and (
        mime_type.startswith(prefix) or mime_type.endswith(suffix)
    )


def get_file_extension(file_path: str) -> str:
    return file_path.split(".")[-1]


def export_audio_file(audio: AudioSegment, filename: str, format: str = "mp3"):
    audio.export(f"{filename}.{format}", format=format)


def is_file_format_supported(format: str) -> bool:
    return format in supported_file_formats


def get_file_name(segment_title: str) -> str:
    for character in invalid_file_name_characters:
        segment_title = segment_title.replace(character, "_")
    return segment_title

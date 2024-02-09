import os
import mimetypes


def file_path_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def verify_mime_type(
    file_path: str, prefix: str = "default", suffix: str = "default"
) -> bool:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mimetypes is not None and (
        mime_type.startswith(prefix) or mime_type.endswith(suffix)
    )

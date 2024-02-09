from utils import file, time
from pydub import AudioSegment


def validate(audio_file_path: str) -> bool:
    return file.file_path_exists(audio_file_path) and file.verify_mime_type(
        audio_file_path, prefix="audio/"
    )


def split_audio_file(audio_file_path: str, timestamps: list):
    print(f"Loading {audio_file_path}")

    audio = AudioSegment.from_file(audio_file_path)

    for i in range(len(timestamps)):
        print(
            f"({i + 1}/{len(timestamps)}) "
            f"Slicing \"{timestamps[i]['song_title']}\""
        )

        start_time = time.convert_to_ms(timestamps[i]["timestamp"])
        end_time = (
            len(audio)
            if i == len(timestamps) - 1
            else time.convert_to_ms(timestamps[i + 1]["timestamp"])
        )

        audio_segment = audio[start_time:end_time]
        audio_segment.export(
            f"{timestamps[i]['song_title']}.mp3", format="mp3"
        )

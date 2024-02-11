def convert_to_ms(timestamp: tuple) -> int:
    hours, minutes, seconds = timestamp

    return (hours * 3600 + minutes * 60 + seconds) * 1000

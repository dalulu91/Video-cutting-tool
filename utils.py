def duration_to_timecode(seconds: int) -> str:
    """Converts seconds (s) to timecode (hh:mm:ss)"""
    hours = int(seconds / 60 / 60)
    hours_sec = hours * 3600
    rest_sec = seconds - hours_sec
    minutes = int(rest_sec / 60)
    minutes_sec = minutes * 60
    rest_sec = rest_sec - minutes_sec
    seconds = int(rest_sec)

    if len(str(hours)) == 1:
        hours = "0" + str(hours)

    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)

    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)

    timecode = f"{hours}:{minutes}:{seconds}"
    return timecode


def format_to_seconds(duration: str) -> int:
    # From: hh:mm:ss
    # To:   ss
    timecode = duration.split(":")
    hours = int(timecode[0]) * 60 * 60
    minutes = int(timecode[1]) * 60
    seconds = int(timecode[2])

    total = seconds + minutes + hours
    return total


def get_duration(start: str, end: str) -> int:
    """Gets duration in seconds"""
    start = format_to_seconds(start)
    end = format_to_seconds(end)
    duration = end - start

    return duration

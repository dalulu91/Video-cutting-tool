def duration_to_timecode(seconds):
    """
    Converts seconds (s) to timecode (hh:mm:ss)
    """
    hours = int(seconds / 60 / 60)  # timer.rest
    hours_sec = hours * 3600  # totalt timer i sekunder
    rest_sec = seconds - hours_sec  # resterende sekunder
    minutes = int(rest_sec / 60)  # minutter.rest
    minutes_sec = minutes * 60  # totalt minutter i sekunder
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


def format_to_seconds(duration):
    # From: hh:mm:ss
    # To:   ss
    timecode = duration.split(":")
    hours = int(timecode[0]) * 60 * 60
    minutes = int(timecode[1]) * 60
    seconds = int(timecode[2])

    total = seconds + minutes + hours
    return total


def timecode_to_seconds(start, end):
    """
    Converts timecode (hh:mm:ss) to seconds (s)
    """
    start = format_to_seconds(start)
    end = format_to_seconds(end)
    duration = end - start

    return duration

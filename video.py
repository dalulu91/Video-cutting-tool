# cut a video with ffmpeg
# import subprocess
import os


def main():
    source = get_input_source()
    start = get_input_start()
    end = get_input_end()
    duration_in_timecode = duration_to_timecode(timecode_to_seconds(start, end))

    print("-ss:", start)
    print("-t:", duration_in_timecode)

    perform_ffmpeg(source, start, duration_in_timecode)


# Functions
def get_input_source():
    source = input("File: ")

    return source


def get_input_start():
    start = input("Start: ")

    return start


def get_input_end():
    end = input("End: ")

    return end


def format_to_seconds(duration):
    # hh:mm:ss
    # 01:02:03
    timecode = duration.split(":")
    hours = int(timecode[0]) * 60 * 60
    minutes = int(timecode[1]) * 60
    seconds = int(timecode[2])

    total = seconds + minutes + hours
    return total


def duration_to_timecode(seconds):
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


def timecode_to_seconds(start, end):
    start = format_to_seconds(start)
    end = format_to_seconds(end)
    duration = end - start

    return duration


def perform_ffmpeg(source, start, duration, output=None):
    # fileext = source.split(".")[:1]
    # output = source + fileext
    if not output:
        output = "nytt_filnavn.mp4"

    shell_command = str(
        "ffmpeg -ss "
        + start
        + " -t "
        + duration
        + " -i "
        + source
        + " -c copy "
        + output
    )

    try:
        os.system(shell_command)
        print("Klipp gjennomført med suksess!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

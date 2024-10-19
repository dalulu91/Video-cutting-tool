# Video Cutter
A simple tool that lets you copy a specific timeframe from a video to a new file.
There's no transcoding going on, so the export is instant.

![python_BoUzWb93oe](https://github.com/user-attachments/assets/fcfcdcc6-d146-4a51-a8d7-c19923f54000)

Requirement: ffmpeg

## How to use
1. Open a video file
2. Adjust the slider position to where you want your new video to begin. *Tip: Use mousewheel to adjust one second increment (windows only)*
3. Set in point by clicking the `[`-button, or press `i` on your keyboard
4. Adjust the slider position to where you want your new video to end
5. Set out point by clicking the `]`-button, or press `o` on your keyboard
6. Click Export and save your new video.

## How does it work?
Video processing is done with ffmepg, so make sure ffmpeg is added to your PATH.
This is the ffmpeg command:

`ffmpeg -ss hh:mm:ss -i input.mp4 -t hh:mm:ss -c copy output.mp4`

`-ss` sets position. `-i` sets input. `-t` sets duration. `-c` sets codec.

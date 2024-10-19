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
It runs ffmepg in shell, so make sure ffmpeg is added to your PATH as an enviornment variable.
This is the shell command:

`ffmpeg -ss hh:mm:ss -t hh:mm:ss -i input.mp4 -c copy output.mp4`

`-ss` sets position. `-t` sets duration. `-i` sets input. `-c` sets codec.

As I'm writing this and reading the documenation, the `-to` would be better to use than `-t`, since that's exactly what this app is doing: Set in pos and out pos. I didn't know that as I wrote the code, so the duration is calculated based on the out position set in the UI.

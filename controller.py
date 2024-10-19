import ui
import tkinter as tk
from tkinter import filedialog
import utils
from moviepy.editor import VideoFileClip
import re

# import os
import subprocess

filepath = ""


app = ui.Window()


def loadfile(event=None):
    filetypes = (("All files", "*.*"),)

    """Event: Open and select video file"""
    file = ui.tk.filedialog.askopenfilename(
        title="Select a video", filetypes=filetypes)
    if file:
        # Update filepath
        global filepath
        filepath = file
        app.headFrame.filepathLabel.configure(text=file)
        set_file_duration(file)


def set_file_duration(filepath):
    """
    1. Gets file duration from opened file.
    2. Updates the slider position.
    # 3. Calls setIn() method
    4. Updates outEntry box
    """

    clip = VideoFileClip(filepath)
    duration = int(clip.duration)

    app.sliderFrame.slider.configure(to=duration)
    app.sliderFrame.max_duration = duration

    # setIn()
    app.timecodeFrame.outStamp.delete("0", tk.END)
    app.timecodeFrame.outStamp.insert(
        "0", utils.duration_to_timecode(duration))

    app.info.configure(
        text=f"Duration:\n{
            utils.duration_to_timecode(duration)}"
    )

    clip.close()


def setIn(event=None):
    """
    Event:
    - Sets in point
    Frontend: Updates Entry-widget
    Backend: sets timecode for -ss parameter in ffmpeg
    """
    app.timecodeFrame.inStamp.delete("0", tk.END)
    app.timecodeFrame.inStamp.insert(
        "0", utils.duration_to_timecode(app.sliderFrame.currentFrame.get())
    )


def setOut(event=None):
    """
    Event:
    Sets out point
    Frontend: Updates Entry-widget
    Backend: sets timecode for -ss parameter in ffmpeg
    """
    app.timecodeFrame.outStamp.delete("0", tk.END)
    app.timecodeFrame.outStamp.insert(
        "0", utils.duration_to_timecode(app.sliderFrame.currentFrame.get())
    )


def saveAs(event=None):
    """
    Event:
    Let's user choose a location and filename
    Returns perform_ffmpeg() and adds a "success"-label
    to the UI.
    """
    source = filepath
    start = app.timecodeFrame.inStamp.get()
    end = app.timecodeFrame.outStamp.get()
    duration = utils.duration_to_timecode(utils.get_duration(start, end))

    filename = filepath.split("/")
    filename = filename[len(filename) - 1]
    name = re.sub(r"\.[a-z0-9]+$", "", filename)
    file_ext = re.search(r"[a-z0-9]+$", filename)
    file_ext = file_ext.group()
    newname = f"{
        name} - {start.replace(":", ".")} - {end.replace(":", ".")} - {duration.replace(":", ".")}.{file_ext}"

    output = filedialog.asksaveasfilename(initialfile=newname)
    if output:
        perform_ffmpeg(source, start, duration, output)

        """ Update logfile and logbox"""
        logFile(output)
        newHeight = int(app.listframe.listbox.cget("height"))
        if newHeight < 5:
            newHeight = newHeight + 1

        app.listframe.listbox.configure(height=newHeight)
        app.listframe.listbox.insert("0", output)


def logFile(filename: str):
    with open("exports.log", "a+") as file:
        file.write(filename)
        file.write("\n")


def perform_ffmpeg(source, start, duration, output):
    # cmd = f'ffmpeg -ss {start} -i "{source}" -t {duration} -c copy "{output}"'
    cmd = [
        "ffmpeg",
        "-ss",
        start,
        "-i",
        source,
        "-t",
        duration,
        "-c",
        "copy",
        output,
    ]

    try:
        subprocess.run(cmd, capture_output=subprocess.DEVNULL)
        # os.system(cmd)
    except Exception as e:
        print(e)


# BINDINGS
app.headFrame.openFileBtn.bind("<Button-1>", loadfile)
app.sliderFrame.setInBtn.bind("<Button-1>", setIn)
app.bind("<i>", setIn, add="+")
app.sliderFrame.setOutBtn.bind("<Button-1>", setOut)
app.bind("<o>", setOut, add="+")
app.exportFrame.exportBtn.bind("<Button-1>", saveAs)


# Run main window
def run():
    app.bind("<Escape>", lambda e: app.destroy())
    app.mainloop()

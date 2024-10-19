import ui
import tkinter as tk
from tkinter import filedialog
import utils
from moviepy.editor import VideoFileClip
import os

filepath = ""


app = ui.Window()


def loadfile(event=None):
    """Event: Open and select video file"""
    file = ui.tk.filedialog.askopenfilename(
        title="Select a video", initialdir=".")
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
    duration = clip.duration

    app.sliderFrame.slider.configure(to=duration)
    app.sliderFrame.max_duration = duration

    # setIn()
    app.timecodeFrame.outStamp.delete("0", tk.END)
    app.timecodeFrame.outStamp.insert(
        "0", utils.duration_to_timecode(duration))

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

    output = filedialog.asksaveasfilename()
    if output:
        perform_ffmpeg(source, start, duration, output)
        # tk.Label(root, text=outputText).pack()

        # TODO: UI Feedback that operation was successful


def perform_ffmpeg(source, start, duration, output):
    shell_command = str(
        "ffmpeg -ss "
        + start
        + " -t "
        + duration
        + ' -i "'
        + source
        + '" -c copy "'
        + output
        + '"'
    )

    try:
        os.system(shell_command)
        print("Klipp gjennomført med suksess!")
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

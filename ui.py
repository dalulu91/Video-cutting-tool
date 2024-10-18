import tkinter as tk
import customtkinter as ctk
import utils


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        style = Style()

        self.minsize(555, 273)
        self.maxsize(1920, 273)
        self.config(background=style.BGCOLOR)
        self.title("Video Cutter")

        self.headFrame = HeadFrame()
        self.timecodeFrame = TimecodeFrame()
        self.sliderFrame = SliderFrame(self.timecodeFrame)
        self.exportFrame = ExportFrame()

        self.headFrame.pack(fill="x", expand=True, anchor="sw", padx=35, pady=15)
        self.sliderFrame.pack(fill="both", expand=True, anchor="n", padx=15)
        self.timecodeFrame.pack(fill="both", expand=True, anchor="n", padx=15)
        self.exportFrame.pack(fill="x", expand=True)


class HeadFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        style = Style()

        self.configure(bg=style.BGCOLOR)

        self.openFileBtn = ctk.CTkButton(
            self, text="Open file", fg_color=style.BTNCOLOR
        )
        self.openFileBtn.pack(side=ctk.LEFT, anchor="nw", padx=(0, 20), pady=5)

        self.filepathLabel = ctk.CTkLabel(
            self,
            text="No files opened yet",
            font=(style.FONT, 14, "italic"),
        )
        self.filepathLabel.pack(side=ctk.LEFT, anchor="nw", pady=5)


class SliderFrame(tk.Frame):
    def __init__(self, timecodeFrame):
        super().__init__()

        style = Style()
        self.timecodeFrame = timecodeFrame

        self.configure(bg=style.BGCOLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=20)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.setInBtn = ctk.CTkButton(
            self,
            text="[",
            width=35,
            fg_color=style.BTNCOLOR,
            font=(style.FONT, 18, "bold"),
        )
        self.setInBtn.grid(row=0, column=0, sticky="e", padx=(10, 0), pady=10)

        self.currentFrame = ctk.DoubleVar()
        self.slider = ctk.CTkSlider(
            self,
            from_=0,
            to=100,
            button_color=style.BTNCOLOR,
            variable=self.currentFrame,
            command=self.refresh_label,
        )
        self.slider.grid(row=0, column=1, sticky="ew", pady=10)

        self.setOutBtn = ctk.CTkButton(
            self,
            text="]",
            width=35,
            fg_color=style.BTNCOLOR,
            font=(style.FONT, 18, "bold"),
        )
        self.setOutBtn.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=10)

        # events
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.slider.bind("<MouseWheel>", self.on_mouse_wheel, add="+")

    def refresh_label(self, event=None):
        self.timecodeFrame.curStamp.set(utils.duration_to_timecode(self.slider.get()))

    def on_mouse_wheel(self, event):
        currentFrame = int(self.slider.get())
        currentStamp = utils.format_to_seconds(self.timecodeFrame.curStamp.get())

        # Check if event is mwheel up
        if event.delta > 0:
            self.slider.set(currentFrame + 1)
            self.timecodeFrame.curStamp.set(
                utils.duration_to_timecode(currentStamp + 1)
            )
        else:
            if self.slider.get() > 0:
                self.slider.set(currentFrame - 1)
                self.timecodeFrame.curStamp.set(
                    utils.duration_to_timecode(currentStamp - 1)
                )


class TimecodeFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        self.configure(bg=style.BGCOLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.inStamp = ctk.CTkEntry(
            self, font=(style.FONT, 18, "bold"), justify="center"
        )
        self.inStamp.grid(
            row=0, column=0, sticky="new", ipadx=25, ipady=5, padx=10, pady=10
        )
        self.inStamp.insert("0", "00:00:00")

        self.curStamp = ctk.StringVar()
        self.curStamp.set("00:00:00")
        self.currentStamp = ctk.CTkLabel(
            self,
            textvariable=self.curStamp,
            font=(style.FONT, 24, "bold"),
        )
        self.currentStamp.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.outStamp = ctk.CTkEntry(
            self, font=(style.FONT, 18, "bold"), justify="center"
        )
        self.outStamp.grid(
            row=0, column=2, sticky="new", ipadx=25, ipady=5, padx=10, pady=10
        )
        self.outStamp.insert("0", "00:00:00")


class ExportFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        self.configure(bg=style.BGCOLOR)

        self.exportBtn = ctk.CTkButton(self, text="Export", fg_color=style.BTNCOLOR)
        self.exportBtn.pack(padx=10, pady=20)


class Style:
    def __init__(self):
        self.BGCOLOR = "#191A1E"
        self.BTNCOLOR = "#64697E"
        self.FONT = "Helvetica"

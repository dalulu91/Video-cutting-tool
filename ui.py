import tkinter as tk
import customtkinter as ctk
import utils


class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        style = Style()

        """ Configure main window """
        self.minsize(555, 273)
        self.maxsize(3000, 273)
        self.config(background=style.BGCOLOR)
        self.title("Video Cutter")

        """ Prepare instances for the main window """
        self.headFrame = HeadFrame()
        self.timecodeFrame = TimecodeFrame()
        self.sliderFrame = SliderFrame(self.timecodeFrame)
        self.exportFrame = ExportFrame()
        self.listframe = ListFrame()
        self.settings = Settings()

        """ Pack instances """
        self.headFrame.pack(fill="x", expand=True,
                            anchor="sw", padx=35, pady=15)
        self.sliderFrame.pack(fill="both", expand=True, anchor="n", padx=15)
        self.timecodeFrame.pack(fill="both", expand=True, anchor="n", padx=15)
        # self.settings.pack(fill="x", expand=True, padx=15)
        self.exportFrame.pack(fill="x", expand=True)
        # self.listframe.pack(fill="x", expand=True)


class HeadFrame(tk.Frame):
    """The HeadFrame contains the "open file"-button"""

    def __init__(self):
        super().__init__()
        style = Style()

        self.configure(bg=style.BGCOLOR)

        """ Open file Button """
        self.openFileBtn = ctk.CTkButton(self)
        self.openFileBtn.configure(text="Open file")
        self.openFileBtn.configure(fg_color=style.BTNCOLOR)
        self.openFileBtn.pack(side=ctk.LEFT, anchor="nw", padx=(0, 20), pady=5)

        """ File path Label """
        self.filepathLabel = ctk.CTkLabel(self)
        self.filepathLabel.configure(self, text="No files opened yet")
        self.filepathLabel.configure(font=(style.FONT, 14, "italic"))
        self.filepathLabel.pack(side=ctk.LEFT, anchor="nw", pady=5)


class SliderFrame(tk.Frame):
    """The SliderFrame contains "Set in/out"-buttons and a slider"""

    def __init__(self, timecodeFrame):
        super().__init__()

        self.timecodeFrame = timecodeFrame
        style = Style()

        self.configure(bg=style.BGCOLOR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=20)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setInBtn = ctk.CTkButton(self)
        self.setInBtn.configure(self, text="[")
        self.setInBtn.configure(self, width=35)
        self.setInBtn.configure(self, fg_color=style.BTNCOLOR)
        self.setInBtn.configure(self, font=(style.FONT, 18, "bold"))
        self.setInBtn.grid(row=0, column=0, sticky="e", padx=(10, 0), pady=10)

        self.currentFrame = ctk.DoubleVar()
        self.slider = ctk.CTkSlider(self)
        self.slider.configure(self, from_=0)
        self.slider.configure(self, to=100)
        self.slider.configure(self, button_color=style.BTNCOLOR)
        self.slider.configure(self, variable=self.currentFrame)
        self.slider.configure(self, command=self.refresh_label)
        self.slider.grid(row=0, column=1, sticky="ew", pady=10)

        self.setOutBtn = ctk.CTkButton(self)
        self.setOutBtn.configure(self, text="]")
        self.setOutBtn.configure(self, width=35)
        self.setOutBtn.configure(self, fg_color=style.BTNCOLOR)
        self.setOutBtn.configure(self, font=(style.FONT, 18, "bold"))
        self.setOutBtn.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=10)

        """ Binds mousewheel event to frame and the slider """
        self.bind("<MouseWheel>", self.mwheel_slide)
        self.slider.bind("<MouseWheel>", self.mwheel_slide, add="+")

    def refresh_label(self, event=None) -> None:
        """Refresh the timecode label with the slider position"""
        pos = self.slider.get()
        self.timecodeFrame.curStamp.set(utils.duration_to_timecode(pos))

    def mwheel_slide(self, event=None) -> None:
        slider_pos = int(self.slider.get())
        max_pos = self.slider.cget("to")
        label = utils.format_to_seconds(self.timecodeFrame.curStamp.get())

        """ Check if moushweel is up (windows only)"""
        if event.delta > 0:
            if slider_pos < max_pos:
                self.slider.set(slider_pos + 1)
                self.timecodeFrame.curStamp.set(
                    utils.duration_to_timecode(label + 1))
        else:
            if slider_pos > 0:
                self.slider.set(slider_pos - 1)
                self.timecodeFrame.curStamp.set(
                    utils.duration_to_timecode(label - 1))


class TimecodeFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        self.configure(bg=style.BGCOLOR)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.inStamp = ctk.CTkEntry(self)
        self.inStamp.configure(self, font=(style.FONT, 18, "bold"))
        self.inStamp.configure(self, justify="center")
        self.inStamp.insert("0", "00:00:00")
        self.inStamp.grid(
            row=0, column=0, sticky="new", ipadx=25, ipady=5, padx=10, pady=10
        )

        self.curStamp = ctk.StringVar()
        self.curStamp.set("00:00:00")
        self.currentStamp = ctk.CTkLabel(self)
        self.currentStamp.configure(self, textvariable=self.curStamp)
        self.currentStamp.configure(self, font=(style.FONT, 24, "bold"))
        self.currentStamp.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        self.outStamp = ctk.CTkEntry(self)
        self.outStamp.configure(self, font=(style.FONT, 18, "bold"))
        self.outStamp.configure(self, justify="center")
        self.outStamp.insert("0", "00:00:00")
        self.outStamp.grid(
            row=0, column=2, sticky="new", ipadx=25, ipady=5, padx=10, pady=10
        )


class ListFrame(tk.Frame):
    def __init__(self):
        super().__init__()
        style = Style()

        self.configure(bg=style.BGCOLOR)
        listbox = tk.Listbox(
            self,
            background=style.BGCOLOR,
            foreground=style.BTNCOLOR,
            font=(style.FONT, 12, "normal"),
        )

        listbox.pack(fill="x", expand=True, padx=15, pady=15)

        exports = []
        with open("exports.log", "r") as file:
            exports.append(file.readlines())

        for export in exports:
            listbox.insert(tk.END, export)

        listbox.insert(tk.END, "First element")
        listbox.insert(tk.END, "First element")
        listbox.insert(tk.END, "First element")


class ExportFrame(tk.Frame):
    def __init__(self):
        super().__init__()

        style = Style()

        self.configure(bg=style.BGCOLOR)

        self.exportBtn = ctk.CTkButton(
            self, text="Export", fg_color=style.BTNCOLOR)
        self.exportBtn.pack(padx=10, pady=20)


class Settings(tk.LabelFrame):
    def __init__(self):
        super().__init__()
        style = Style()

        self.configure(
            text="Settings",
            background=style.BGCOLOR,
            foreground=style.BTNCOLOR,
            borderwidth=0,
        )

        self.copyCodec = ctk.CTkCheckBox(self, text="Copy codec")
        self.copyCodec.select()
        self.copyCodec.pack()

        self.qualityLabel = ctk.CTkLabel(self, text="Set quality")
        self.qualityLabel.pack()

        self.qualityscale = ctk.CTkSlider(self, from_=0, to=100)
        self.qualityscale.set(100)
        self.qualityscale.pack()


class Style:
    def __init__(self):
        self.BGCOLOR = "#191A1E"
        self.BTNCOLOR = "#64697E"
        self.FONT = "Helvetica"

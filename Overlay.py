import time

from tkinter import *
from math import *
from configparser import ConfigParser

KEY_COLOR = "#000000"

class Overlay:
    width = None
    height = None

    window = None
    canvas = None

    def __init__(self, title, width, height):
        self.width = width
        self.height = height
        window = Tk()
        window.wm_geometry(str(self.width) + "x" + str(self.height))
        window.title(title)
        self.window = window

        canvas = Canvas(window, bg=KEY_COLOR)
        canvas.pack(fill=BOTH, expand=1)
        self.canvas = canvas


class HideableOverlay(Overlay):

    visible = False
    should_be_visible = False

    color = None
    element_id = None

    def __init__(self, color):
        self.color = color

    def set_visibility(self, visibility):
        self.should_be_visible = visibility

    # to be called in something that can catch an error
    def update_visibility(self):
        if self.visible != self.should_be_visible:
            if isinstance(self.element_id, list):
                for element in self.element_id:
                    self.canvas.itemconfig(element, fill=self.color if self.should_be_visible else KEY_COLOR)
            else:
                self.canvas.itemconfig(self.element_id, fill=self.color if self.should_be_visible else KEY_COLOR)
            self.visible = self.should_be_visible


class CountdownTimer(HideableOverlay):
    start_time = None
    seconds = None
    COLOR = "red"

    def __init__(self):
        Overlay.__init__(self, "Timer", 500, 500)
        HideableOverlay.__init__(self, self.COLOR)

        self.element_id = self.canvas.create_text(self.width/2, self.height/2, text="00", fill=KEY_COLOR, font=("Arial", 300), tag="timer")

    def set_timer(self, seconds:int):
        self.start_time = time.time()
        self.seconds = seconds
        self.should_be_visible = True

    def tick(self):
        remaining = int(self.seconds - (time.time() - self.start_time))
        display = max(0, remaining)
        try:
            self.update_visibility()

            if self.start_time is not None and remaining < -5:
                self.canvas.itemconfig(self.element_id, fill=KEY_COLOR)
            self.canvas.itemconfig(self.element_id, text="{0:0=2d}".format(display))
            self.canvas.update()

        except TclError as exception:
            #window has been destroyed (probably Xed out)
            return False


        return True


class Label(HideableOverlay):

    text = None
    COLOR = "red"
    font = "Arial"
    font_size=None

    def __init__(self, title, width=1200, height=600, font_size=300):
        Overlay.__init__(self, title, width, height)
        HideableOverlay.__init__(self, self.COLOR)
        self.element_id = self.canvas.create_text(self.width/2, self.height/2, fill=KEY_COLOR, font=(self.font, font_size), tag="timer")
        self.font_size = font_size

    def set_text(self, text, font_size=None):
        self.text = text
        self.should_be_visible = True
        self.font_size = font_size if font_size is not None else self.font_size

    def tick(self):
        try:
            if self.text is not None:
                self.canvas.itemconfig(self.element_id, text=self.text, font=(self.font, self.font_size))
                self.text = None

            self.update_visibility()
            self.canvas.update()

        except TclError as exception:
            #window has been destroyed (probably Xed out)
            return False


class TextGrid(HideableOverlay):

    element_id = []

    text = []
    COLOR = "red"
    font = "Arial"

    def __init__(self, title, font_size=50, color="red"):
        HideableOverlay.__init__(self, color)

        config = ConfigParser()
        config.read("GrimBot.ini")
        grid_width = config.getint("Draft", "GridWidth")
        grid_height = config.getint("Draft", "GridHeight")
        Overlay.__init__(self, title, grid_width, grid_height)

        column_offset = round(grid_width * config.getfloat("Draft", "ColumnOffset"))
        row_offset = round(grid_height * config.getfloat("Draft", "RowOffset"))
        column_spacing = round(grid_width * config.getfloat("Draft", "ColumnSpacing"))
        row_spacing = round(grid_height * config.getfloat("Draft", "RowSpacing"))


        for i in range(0, 12):
            self.element_id.append(self.canvas.create_text(
                                                    column_offset + column_spacing * (i % 4),
                                                    row_offset + row_spacing * int(i / 4),
                                                    fill=KEY_COLOR,
                                                    font=(self.font, font_size),
                                                    tag="text" + str(i)))

        self.calibrate_on = config.getboolean("Draft", "CalibrateMode")

    def set_text(self, text_array):
        self.text = text_array
        self.should_be_visible = True

    def tick(self):

        try:
            if len(self.text) > 0:
                for i in range(0, len(self.text)):
                    self.canvas.itemconfig(self.element_id[i], text=self.text[i])
                self.text = []
            if self.calibrate_on:
                self.reposition_numbers()
            self.update_visibility()
            self.canvas.update()

        except TclError as exception:
            # window has been destroyed (probably Xed out)
            return False

    def reposition_numbers(self):
        config = ConfigParser()
        config.read("GrimBot.ini")
        grid_width = config.getint("Draft", "GridWidth")
        grid_height = config.getint("Draft", "GridHeight")

        column_offset = round(grid_width * config.getfloat("Draft", "ColumnOffset"))
        row_offset = round(grid_height * config.getfloat("Draft", "RowOffset"))
        column_spacing = round(grid_width * config.getfloat("Draft", "ColumnSpacing"))
        row_spacing = round(grid_height * config.getfloat("Draft", "RowSpacing"))

        for element in self.element_id:
            self.canvas.itemconfig(element, text="O")
            self.canvas.coords(element,
                               column_offset + column_spacing * ((element - 1) % 4),
                               row_offset + row_spacing * int((element - 1) / 4))

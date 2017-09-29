from tkinter import *
from tkinter import font as tkFont


class Incrementer:
    callbacks = []

    def __init__(self, parent_frame, value: IntVar, gui):
        self.gui = gui
        helv36 = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)

        self.the_variable = value


        self.frame = Frame(parent_frame, height=500, width=150)
        self.frame.grid(row=0, columnspan=3)
        self.frame.columnconfigure(0, minsize=100)
        self.frame.columnconfigure(1, minsize=100)
        self.frame.columnconfigure(2, minsize=100)

        decrement_button = Button(self.frame,
                                  text="-",
                                  width=3,
                                  height=1,
                                  font=helv36,
                                  command=self.decrement_value)
        decrement_button.grid(row=0, column=0)

        value_display = Label(self.frame,
                              textvariable=self.the_variable,
                              font=helv36)
        value_display.grid(row=0, column=1)

        increment_button = Button(self.frame,
                                  text="+",
                                  width=3,
                                  height=1,
                                  font=helv36,
                                  command=self.increment_value)
        increment_button.grid(row=0, column=2)

    def increment_value(self):
        self.the_variable.set(self.the_variable.get() + 1)
        self.gui.stop_poll()

    def decrement_value(self):
        self.the_variable.set(self.the_variable.get() - 1)
        self.gui.stop_poll()

    def grid(self, row=None, column=None,):
        self.frame.grid(column=column, row=row)



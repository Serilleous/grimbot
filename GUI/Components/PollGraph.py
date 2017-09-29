from tkinter import *
from tkinter import font as tkFont
from configparser import ConfigParser
import RoboGrimConfig


class PollGraph:
    def __init__(self, canvas: Canvas, card_in_pack, state):
        self.state = state

        self.margin_left = 100
        self.margin_right = 130
        self.bar_border = 4
        self.card_in_pack = card_in_pack

        self.font = tkFont.Font(family='Helvetica', size=16, weight=tkFont.BOLD)
        self.small_font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        spacing = canvas.winfo_height() / 13

        config = ConfigParser()
        config.read(RoboGrimConfig.CONFIG)
        primary_color = config.get('Poll', 'PrimaryColor')
        secondary_color = config.get('Poll', 'SecondaryColor')
        self.canvas = canvas

        ypos = spacing * self.card_in_pack

        self.background_line = canvas.create_line(self.margin_left - self.bar_border,
                                                  ypos,
                                                  canvas.winfo_width() - self.margin_right + self.bar_border,
                                                  ypos,
                                                  fill=secondary_color,
                                                  width=20 + self.bar_border * 2)
        self.line = canvas.create_line(self.margin_left,
                                       ypos,
                                       canvas.winfo_width() - self.margin_right,
                                       ypos,
                                       fill=primary_color,
                                       width=20)

        self.card_number = canvas.create_text(self.margin_left / 2,
                                              ypos,
                                              text=self.card_in_pack,
                                              font=self.font,
                                              fill=primary_color)
        self.percentage = canvas.create_text(canvas.winfo_width() - self.margin_right / 2,
                                             ypos,
                                             text='%99',
                                             font=self.small_font,
                                             fill=primary_color)
        canvas.winfo_width()
        canvas.after(0, self.update_graph)

    def update_graph(self):
        self.canvas.after(100, self.update_graph)

        if 13 - self.state.pick.get() < self.card_in_pack:
            self.hide()
        else:
            self.show()

        spacing = self.canvas.winfo_height() / 13
        ypos = spacing * self.card_in_pack

        max_line_length = self.canvas.winfo_width() - (self.margin_left + self.margin_right)
        total_votes = sum(self.state.votes)
        our_votes = self.state.votes[self.card_in_pack - 1]
        percentage = 0 if our_votes == 0 else our_votes/total_votes
        self.canvas.coords(self.background_line,
                           self.margin_left - self.bar_border,
                           ypos,
                           self.canvas.winfo_width() - self.margin_right + self.bar_border,
                           ypos)
        self.canvas.coords(self.line,
                           self.margin_left,
                           ypos,
                           self.margin_left + max_line_length * percentage,
                           ypos)
        self.canvas.coords(self.card_number,
                           self.margin_left / 2,
                           ypos)
        self.canvas.coords(self.percentage,
                           self.canvas.winfo_width() - self.margin_right / 2,
                           ypos)
        self.canvas.itemconfigure(self.percentage,
                                  text='%' + str(round(percentage * 100)))


    def hide(self):
        self.canvas.itemconfigure(self.background_line, state='hidden')
        self.canvas.itemconfigure(self.line, state='hidden')
        self.canvas.itemconfigure(self.card_number, state='hidden')
        self.canvas.itemconfigure(self.percentage, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.background_line, state='normal')
        self.canvas.itemconfigure(self.line, state='normal')
        self.canvas.itemconfigure(self.card_number, state='normal')
        self.canvas.itemconfigure(self.percentage, state='normal')

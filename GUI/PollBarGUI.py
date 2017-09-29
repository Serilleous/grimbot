from tkinter import *
from GUI.Components import PollGraph
from configparser import ConfigParser
import RoboGrimConfig

class PollBarGUI:
    def __init__(self, root, state):
        self.root = root
        self.state = state

        config = ConfigParser()
        config.read(RoboGrimConfig.CONFIG)
        background_color = config.get('Poll', 'BackgroundColor')

        window = Toplevel(root)
        window.geometry('500x800')
        window.title('Poll Graph')
        canvas = Canvas(window)
        canvas.pack(fill=BOTH, expand=1)
        canvas.configure(background=background_color)

        graph_bars = []
        for i in range(1, 13):
            graph_bars.append(PollGraph.PollGraph(canvas, i, self.state))

        self.root.after(0, self.update_state)

    def update_state(self):


        self.root.after(100, self.update_state)
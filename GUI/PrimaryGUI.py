from tkinter import *
from tkinter import font as tkFont


from GUI.Components import Incrementer
from GUI import PollBarGUI
import PollDraftState


class PrimaryGUI:
    def __init__(self, root, poll_state: PollDraftState):
        self.root = root
        self.poll_state = poll_state

        helv36 = tkFont.Font(family='Helvetica', size=16)#, weight=tkFont.BOLD)

        root.geometry('700x500')
        root.resizable(width=FALSE, height=FALSE)
        root.title("Grimbot")
        root.grid()

        pack_label = Label(root, text="Pack Number")
        pack_label.grid(row=0, columnspan=3)

        pack_incrementer = Incrementer.Incrementer(root, self.poll_state.pack, self)
        pack_incrementer.grid(row=1)

        pick_label = Label(root, text="Pick Number")
        pick_label.grid(row=0, column=3, columnspan=3)
        pick_incrementer = Incrementer.Incrementer(root, self.poll_state.pick, self)
        pick_incrementer.grid(row=1, column=3)

        self.start_button = Button(root,
                              text="Start Poll",
                              font=helv36,
                              command=self.start_poll)
        self.start_button.grid(row=2, column=0, pady=(50, 0), columnspan=3, sticky=E+W)

        self.stop_button = Button(root, text="Reset Poll", font=helv36)
        self.stop_button.grid(row=2, column=3, pady=(50, 0), columnspan=3, sticky=E+W)

        open_graph_button = Button(root,
                                   text="Open poll graph",
                                   command=self.open_graph)
        open_graph_button.grid(row=3, pady=(50, 0))

        self.next_pack_button = Button(root,
                                      text="Next pack",
                                      command=self.next_pack)
        self.next_pack_button.grid(row=3, column=3, pady=(50,0))
        self.next_pack_button.grid_remove()


    def increment_value(self):
        pass

    def open_graph(self):
        PollBarGUI.PollBarGUI(self.root, self.poll_state)

    def start_poll(self):
        self.poll_state.currently_polling = True
        self.start_button.config(text="Next Card",
                                 command=self.next_card)
        self.stop_button.config(text="Stop Poll",
                                command=self.stop_poll)
        self.next_pack_button.grid()

    def next_card(self):
        self.poll_state.next_card = True

    def next_pack(self):
        self.poll_state.next_pack = True

    def reset_poll(self):
        self.poll_state.reset()
        self.start_button.config(text='Start Poll',
                                 command=self.start_poll)
        self.next_pack_button.grid_remove()

    def stop_poll(self):
        self.poll_state.currently_polling = False
        self.stop_button.config(text="Reset Poll",
                                command=self.reset_poll)
        self.start_button.config(text='Start Poll',
                                 command=self.start_poll)
        self.next_pack_button.grid_remove()

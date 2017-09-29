from tkinter import IntVar

class PollState:

    def __init__(self):
        self.pack = IntVar(value=1)
        self.pick = IntVar(value=1)
        self.reset()


    def reset(self):
        self.fresh_poll = True
        self.currently_polling = False
        self.next_card = False
        self.next_pack = False
        self.votes = [0] * 12
        self.pack.set(value=1)
        self.pick.set(value=1)
        self.user_voted = []

    def get_valid_votes(self):
        return list(range(1, 14 - self.pick.get()))

    def reset_vote_tracking(self):
        self.user_voted = []
        self.votes = [0] * 12

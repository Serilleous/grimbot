import PollDraftState
import GrimCommunicator
from tkinter import IntVar


class PollDraft:
    communicator = None
    active_mode = None
    state = None

    def __init__(self, communicator: GrimCommunicator, state: PollDraftState):
        self.communicator = communicator
        self.state = state
        self.active_mode = PollDraftIdle(self.state, communicator)
        pass

    def input(self, username, message):
        self.active_mode.input(username, message)

    def start(self):
        pass

    def tick(self):
        # tick the phase and move to the next on if appropriate
        should_continue, next_phase = self.active_mode.tick()

        if next_phase is not None:
            self.active_mode = next_phase

        return should_continue


class PollDraftMode:
    state: PollDraftState = None

    def __init__(self, state: PollDraftState, communicator):
        self.state = state
        self.communicator = communicator
        pass

    def input(self, username, message):
        pass

    def tick(self):
        return True, None


class PollDraftIdle(PollDraftMode):

    def __init__(self, state: PollDraftState, communicator):
        super(PollDraftIdle, self).__init__(state, communicator)


    def tick(self):
        if self.state.currently_polling:
            return True, PollDraftActive(self.state, self.communicator)
        return True, None


class PollDraftActive(PollDraftMode):

    def __init__(self, state: PollDraftState, communicator):
        super(PollDraftActive, self).__init__(state, communicator)
        self.state.reset_vote_tracking()
        self.communicator.chat("Draft poll starting, Valid choices are: " + ''.join(str(e) + ' ' for e in self.state.get_valid_votes()))


    def tick(self):
        if not self.state.currently_polling:
            return True, PollDraftIdle(self.state, self.communicator)

        if self.state.next_card:
            next_card(self.state)
            self.communicator.chat("Draft poll starting, Valid choices are: " + ''.join(str(e) + ' ' for e in self.state.get_valid_votes()))

        if self.state.next_pack:
            next_pack(self.state)
            self.communicator.chat("Draft poll starting, Valid choices are: " + ''.join(str(e) + ' ' for e in self.state.get_valid_votes()))
        return True, None

    def input(self, username, message):
        messageValue = None
        try:
            messageValue = int(message)
        except:
            pass
        if messageValue and messageValue in self.state.get_valid_votes() and not any(username in s for s in self.state.user_voted):
            print(username + ' voted for ' + message)
            self.state.user_voted.append(username)
            self.state.votes[messageValue - 1] += 1
        return True, None

def next_card(state):
    state.reset_vote_tracking()
    pick = state.pick.get() + 1
    pack = state.pack.get()
    if pick > 12:
        pick = 1
        pack = pack + 1

    state.pick.set(pick)
    state.pack.set(pack)

    state.next_card = False

def next_pack(state):
    state.reset_vote_tracking()
    state.pick.set(value=1)
    state.pack.set(value=state.pack.get() + 1)
    state.next_pack = False

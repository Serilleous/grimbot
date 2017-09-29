
from Modules import PollDraft
import PollDraftState

class ModuleManager:
    active_module = None

    def __init__(self, poll_state: PollDraftState):
        self.poll_state = poll_state

    def start_poll_module(self):
        self.start_module(PollDraft.PollDraft(self.poll_state))

    def start_module(self, new_module):
        self.active_module = new_module
        self.active_module.start()

    def stop_module(self):
        self.active_module = None

    def tick(self):
        if self.active_module is None:
            return

        should_continue = self.active_module.tick()
        if should_continue is False:
            self.stop_module()

    def input(self, username, message):
        if self.active_module is not None:
            self.active_module.input(username, message)

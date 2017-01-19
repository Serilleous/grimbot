import pyperclip


class CopyChat:

    communicator = None

    def __init__(self, communicator):
        print("CopyBot Initialized.")
        self.communicator = communicator

    def input(self, username, message):
        # Copy input to clipboard if I am grimfan
        pyperclip.copy(message)

    def start(self):
        pass

    def tick(self):
        pass
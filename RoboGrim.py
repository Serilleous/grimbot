import re

import GrimCommunicator
import MessageHandler
import RoboGrimConfig
import Modules.ModuleManager
import time
import GUI.PrimaryGUI
import PollDraftState

from tkinter import *

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# todo:  make this less shitty (more modular)
poll_state = None


def main_loop(root):
    communicator = GrimCommunicator.GrimCommunicator()
    module_manager = Modules.ModuleManager.ModuleManager(poll_state)
    handler = MessageHandler.MessageHandler(communicator, module_manager, poll_state)


    while communicator.connected:

        root.update_idletasks()
        root.update()

        response = communicator.get_next_message()

        if response == "PING :tmi.twitch.tv\r\n":
            communicator.pong_server()
            continue
        elif response is not None:
            handler.handle_response(response)

        if response is not None:
            encoded_response = response.encode("utf-8")
            print(encoded_response)

        module_manager.tick()

        time.sleep(1 / RoboGrimConfig.RATE)


if __name__ == "__main__":
    root = Tk()
    poll_state = PollDraftState.PollState()
    gui = GUI.PrimaryGUI.PrimaryGUI(root, poll_state)
    main_loop(root)


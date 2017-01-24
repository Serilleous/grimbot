import re

import GrimCommunicator
import MessageHandler
import RoboGrimConfig
import Modules.ModuleManager
import time

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


def main_loop():

    communicator = GrimCommunicator.GrimCommunicator()
    module_manager = Modules.ModuleManager.ModuleManager()
    handler = MessageHandler.MessageHandler(communicator, module_manager)


    active_module = None

    while communicator.connected:

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
    main_loop()


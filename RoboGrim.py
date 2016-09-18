import re
from time import sleep
import socket
import Draft
import RoboGrimConfig
import GrimCommunicator
import MessageHandler

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


def main_loop():

    communicator = GrimCommunicator.GrimCommunicator()
    handler = MessageHandler.MessageHandler(communicator)

    while communicator.connected:

        response = communicator.get_next_message()

        if response == "PING :tmi.twitch.tv\r\n":
            communicator.pong_server()
            continue
        else:
            handler.handle_response(response)

        print(response)


'''
        if response == "PING :tmi.twitch.tv\r\n":
            ourSocket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

        sleep(1/RoboGrimConfig.RATE)
        communicator.chat(communicator, "test")
'''

'''

    while connected:
        response = ourSocket.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            ourSocket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
        test = re.search(r"\w+", response)

        # Parse the message!
        if message == "!test\r\n":
            chat("Testing successful I guess.\r\n")

        if message == "!tts\r\n":
            chat("Because he works in a computer lab Grimfan uses text to speech to communicate out of respect for his co-workers and students that use the lab as a resource.\r\n")

        if message == "!draft\r\n" and username == "grimfan":
            active_module = Draft.Draft()

        if message == "!stopdraft\r\n" and username == "grimfan":
            active_module = "none"

        if active_module != "none":
            active_module.input(message)

        print(username + ": " + message)
        sleep(1 / RATE)


def chat(msg):
    ourSocket.send("PRIVMSG {} :{}".format(RoboGrimConfig.CHAN, msg).encode())
'''
if __name__ == "__main__":
    main_loop()


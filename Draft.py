import RoboGrimConfig
import RoboGrim
import socket
import re


class Draft:
    def __init__(self):
        print("Draft Started.")

    def mydraft(self):
        # chat(sock, "Starting Your Draft Duder!\r\n")
        draft = True

        match = int(re.search("(?<=!)\d+(?=\r\n)", RoboGrim.CHAT_MSG))
        print(match)

    def input(self, input):
        RoboGrim.chat("got it!")
import re
from time import sleep
import socket
import mydraft
import RoboGrimConfig



RATE = (20 / 30)
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

def main_loop():
    message = ""
    try:
        s = socket.socket()
        s.connect((RoboGrimConfig.HOST, RoboGrimConfig.PORT))
        s.send("PASS {}\r\n".format(RoboGrimConfig.PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(RoboGrimConfig.NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(RoboGrimConfig.CHAN).encode("utf-8"))
        connected = True
    except Exception as e:
        print(str(e))
        connected = False

    while connected:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)


        if message == "!test\r\n":
            chat(s, "Testing successful I guess.\r\n")

        if message == "!tts\r\n":
            chat(s, "Because he works in a computer lab Grimfan uses text to speech to communicate out of respect for his co-workers and students that use the lab as a resource.\r\n")

        if message == "!draft\r\n":
            mydraft.mydraft(s)

        print(username + ": " + message)
        sleep(1 / RATE)

def chat(sock, msg):
    sock.send("PRIVMSG {} :{}".format(RoboGrimConfig.CHAN, msg).encode())

if __name__ == "__main__":
    main_loop()


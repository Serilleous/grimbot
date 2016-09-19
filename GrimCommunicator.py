import socket
import RoboGrimConfig


class GrimCommunicator:

    active_socket = None
    connected = None

    def __init__(self):
        try:
            self.active_socket = socket.socket()
            self.active_socket.connect((RoboGrimConfig.HOST, RoboGrimConfig.PORT))
            self.active_socket.send("PASS {}\r\n".format(RoboGrimConfig.PASS).encode("utf-8"))
            self.active_socket.send("NICK {}\r\n".format(RoboGrimConfig.NICK).encode("utf-8"))
            self.active_socket.send("JOIN {}\r\n".format(RoboGrimConfig.CHAN).encode("utf-8"))
            self.active_socket.setblocking(0)
            self.connected = True
            print("Successfully Connected")
        except Exception as exception:
            print(str(exception))
            self.connected = False

    def pong_server(self):
        self.active_socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("PONG")

    def chat(self, message):
        self.active_socket.send("PRIVMSG {} :{}".format(RoboGrimConfig.CHAN, str(message) + "\r\n").encode("utf-8"))

    def get_next_message(self):
        next_message = None
        try:
            next_message = self.active_socket.recv(1024).decode("utf-8")
        except Exception as exception:
            # do nothing if there's no message :\
            pass
        return next_message





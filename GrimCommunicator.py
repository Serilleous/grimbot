import socket
import RoboGrimConfig


class GrimCommunicator:

    activeSocket = None
    connected = None

    def __init__(self):
        try:
            activeSocket = socket.socket()
            activeSocket.connect((RoboGrimConfig.HOST, RoboGrimConfig.PORT))
            activeSocket.send("PASS {}\r\n".format(RoboGrimConfig.PASS).encode("utf-8"))
            activeSocket.send("NICK {}\r\n".format(RoboGrimConfig.NICK).encode("utf-8"))
            activeSocket.send("JOIN {}\r\n".format(RoboGrimConfig.CHAN).encode("utf-8"))
            connected = True
            print("Successfully Connected")
        except Exception as exception:
            print(str(exception))
            connected = False
     

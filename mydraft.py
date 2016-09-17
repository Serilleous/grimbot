import RoboGrimConfig
import pyautogui
import RoboGrim
import socket
import re


pyautogui.PAUSE = 5

def mydraft(sock):
    print("Draft Started.")
    # chat(sock, "Starting Your Draft Duder!\r\n")
    draft = True

    while draft == True:
        vote=[0]*13

        match = int(re.search("(?<=!)\d+(?=\r\n)", RoboGrim.CHAT_MSG))
        print(match)

      #  if RoboGrim.CHAT_MSG == "!1\r\n":
           # vote[1] += 1
       # if RoboGrim.CHAT_MSG == "!2\r\n":
           # vote[2] += 1
       # if RoboGrim.CHAT_MSG == "!3\r\n":
            #vote[3] += 1
      #  if RoboGrim.CHAT_MSG == "!4\r\n":
            #vote[4] += 1
      #  if RoboGrim.CHAT_MSG == "!5\r\n":
            #vote[5] += 1
      #  if RoboGrim.CHAT_MSG == "!6\r\n":
           # vote[6] += 1
     #   if RoboGrim.CHAT_MSG == "!7\r\n":
            #vote[7] += 1
       # if RoboGrim.CHAT_MSG == "!8\r\n":
           # vote[8] += 1
     #   if RoboGrim.CHAT_MSG == "!9\r\n":
          #  vote[9] += 1
    #    if RoboGrim.CHAT_MSG == "!10\r\n":
           # vote[10] += 1
      #  if RoboGrim.CHAT_MSG == "!11\r\n":
          #  vote[11] += 1
    #    if RoboGrim.CHAT_MSG == "!12\r\n":
          #  vote[12] += 1

def chat(sock, msg):
    sock.send("PRIVMSG {} :{}".format(RoboGrimConfig.CHAN, msg).encode())



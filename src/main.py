from distutils.command.config import config
import ttvController as ttv
import socket, time
from config import *


def main(): 

    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'newtwitchplaysosrs'

    sock = socket.socket()

    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    print("Started")

    ttvCont = ttv.TtvController()

    while True:
        resp = sock.recv(2048).decode('utf-8')
        #print(resp)

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            try:
                ttvCont.readChat(resp)
            except Exception as e: 
                print(e)
        
        time.sleep(7)


# main()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        ttvCont.parseChat("ra4")
    except Exception as e: 
        print(e)

# time.sleep(4)
testSingle()
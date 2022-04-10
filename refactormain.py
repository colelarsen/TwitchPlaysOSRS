import ttvController as ttv
import socket, time


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

    ttvCont = ttv()

    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            print(resp)
            try:
                ttvCont.readChat(resp)
            except:
                print("An exception occurred")
        
        time.sleep(0.6)


main()
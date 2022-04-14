from distutils.command.config import config
import ttvController as ttv
import socket, time
from config import *
import pytchat
import threading
import discordReader
import queue
import fileHandler

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'newtwitchplaysosrs'
youtubeVideoId = 'Q41OiZqu87c'


ttvCont = ttv.TtvController()

#Function that reads chat from twitch
def mainTTV(commandList, messageQueue): 
    sock = socket.socket()

    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    print("Started")


    while True:
        resp = sock.recv(2048).decode('utf-8')
        #print(resp)

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            try:
                resp = resp.rstrip().split('\r\n')
                for i in resp:
                    if "PRIVMSG" in i:
                        line = i
                        user = line.split(':')[1].split('!')[0]
                        msg = line.split(':', maxsplit=2)[2]
                        line = user + ": " + msg

                        fileHandler.addLineToQueue("Twitch: " + line, messageQueue)

                        msg = msg.lower()
                        msg = msg.strip()
                        commandList.append(msg)
                        
            except Exception as e: 
                print(e)
        
        time.sleep(0.1)

#Function that reads chat from Youtube
def mainYT(commandList, messageQueue):
    print("Started")
    chat = pytchat.create(video_id=youtubeVideoId)

    while chat.is_alive():
        try:
            data = chat.get()
            items = data.items
            for c in items:
                msg = c.message
                msg = msg.lower()
                msg = msg.strip()
                commandList.append(msg)
                messageQueue.put(msg)
            # time.sleep(0.5)
        except KeyboardInterrupt:
            chat.terminate()
            break

#Function that reads chat from Discords
def mainDiscord(commandList, messageQueue):
    discordBot = discordReader.DiscordBot(commandList, messageQueue)

    discordBot.run(discordBotLogin)

commands = []
messageQueue = queue.Queue()

#Main function gets what all other threads have added to command list and reads them through the parser
def main(commandList, messageQueue):
    counter = 0
    while True:
        ttvCont.readChat(commandList)
        commandList.clear()
        time.sleep(0.2)
        if counter > 50:
            ttvCont.checkLoginScreen()
            ttvCont.checkBankScreen()
        fileHandler.writeQueueToFile("chatHistory.txt", messageQueue)


#Start TTV thread
mainTTVThread = threading.Thread(target=mainTTV, args=(commands, messageQueue,))
mainTTVThread.start()

#Start Youtube thread
# mainYTThread = threading.Thread(target=mainYT, args=())
# mainYTThread.start()

#Start main thread
mainThread = threading.Thread(target=main, args=(commands, messageQueue))
mainThread.start()

#Start Discord thread
mainDiscord(commands, messageQueue)


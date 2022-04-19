from distutils.command.config import config
import ttvController as ttv
import socket, time
from config import *
import pytchat
import threading
import discordReader
import queue
import fileHandler
import messageHandler


server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'newtwitchplaysosrs'
youtubeVideoId = 'Q41OiZqu87c'

messages = messageHandler.messageHandler("chatHistory.txt")


ttvCont = ttv.TtvController()

#Function that reads chat from twitch
def mainTTV(messages): 
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


                        messages.get_message( "ttv", user, msg)
                        
            except Exception as e: 
                print(e)
        
        time.sleep(0.1)

#Function that reads chat from Discords
def mainDiscord(messageHandler):
    discordBot = discordReader.DiscordBot(messageHandler)

    discordBot.run(discordBotLogin)

commands = []


#Main function gets what all other threads have added to command list and reads them through the parser
def main(messages):
    counter = 0
    while True:
        ttvCont.readChat(messages.commands)

        if not messages.commands.empty():
            messages.writeChatToFile()
            messages.clear_commands()

        time.sleep(0.2)
        counter += 1
        if counter > 50:
            counter = counter - 50
            ttvCont.screen_check()
            messages.close_chat_file()
            
        


#Start TTV thread
mainTTVThread = threading.Thread(target=mainTTV, args=(messages,))
mainTTVThread.start()

#Start Youtube thread
# mainYTThread = threading.Thread(target=mainYT, args=())
# mainYTThread.start()

#Start main thread
mainThread = threading.Thread(target=main, args=(messages,))
mainThread.start()

#Start Discord thread
mainDiscord(messages)










## DEPRECIATED
#Function that reads chat from Youtube
# def mainYT(commandList, messageQueue):
#     print("Started")
#     chat = pytchat.create(video_id=youtubeVideoId)

#     while chat.is_alive():
#         try:
#             data = chat.get()
#             items = data.items
#             for c in items:
#                 msg = c.message
#                 msg = msg.lower()
#                 msg = msg.strip()
#                 commandList.append(msg)
#                 messageQueue.put(msg)
#             # time.sleep(0.5)
#         except KeyboardInterrupt:
#             chat.terminate()
#             break
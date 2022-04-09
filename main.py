import socket, time
from tkinter.tix import MAX

from pyperclip import waitForNewPaste
from imagesearch import *
import pyautogui
import re
from config import *

print("Startin Socket")

#Get inputs from Twitch Chat
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'newtwitchplaysosrs'



sock = socket.socket()










def calibration():
    moveMouse(startingMainSquareX,startingMainSquareY)
    for i in range(0, 20):
        for j in range(0, 13):
            moveMouse(startingMainSquareX + mainSquareWidth*i, startingMainSquareY + mainSquareHeight*j)
            time.sleep(0.001)
    
    moveMouse(invStartingX,invStartingY)
    for i in range(0, 4):
        for j in range(0, 7):
            moveMouse(invStartingX + invSquareWidth*i, invStartingY + invSquareHeight*j)
            time.sleep(0.01)


def main(): 
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    print("Started")

    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))
        
        elif len(resp) > 0:
            print(resp)
            try:
                readChat(resp)
            except:
                print("An exception occurred")
        
        time.sleep(0.6)

#Parse input with safe regex into commands0

def readChat(resp):
    resp = resp.rstrip().split('\r\n')
    line = random.choice(resp)
    if "PRIVMSG" in line:
        user = line.split(':')[1].split('!')[0]
        msg = line.split(':', maxsplit=2)[2]
        line = user + ": " + msg
        parseChat(msg)


def parseChat(lineRaw):  

    line = lineRaw.lower()
    print(line)

    tester = imagesearch("loginscreen.PNG", 0.8)
    bankPin = imagesearch("bankPin.PNG", 0.8)
    if tester[0] == -1 and bankPin[0] == -1:
    
        #ilc 1-28 click inventory spot
        if "ilc" in line or (line[0]=='i' and line[1]==' ' and line[3].isnumeric()): 
            #perform left click on coordinates given
            coords = line.split(' ')[1].strip()
            num = int(re.split("[^\d]", coords)[1])
            if coords[0] in ['a', 'b', 'c', 'd'] and num < 8 and num >= 0:
                leftClickInv(coords[0], num)
        elif line[0]=='i' and line[1] in ['a', 'b', 'c', 'd'] and line[2].isnumeric():
            num = int(line[2])
            if num < 8 and num >= 0:
                leftClickInv(line[1], num)

        elif line.startswith("drop "): 
            #perform left click on coordinates given
            coords = line.split(' ')[1].strip()
            num = int(re.split("[^\d]", coords)[1])
            if coords[0] in ['a', 'b', 'c', 'd'] and num < 8 and num >= 0:
                dropItem(coords[0], num)

        elif line.startswith("mm "): 
            dir = line.split(' ')
            if(dir[1] == "top" or dir[1] == "t"):
                moveMouse(650, 40)
                time.sleep(0.25)
                pyautogui.click()
            if(dir[1] == "bottom" or dir[1] == "bot" or dir[1] == "b"):
                moveMouse(650, 160)
                time.sleep(0.25)
                pyautogui.click()
            if(dir[1] == "left" or dir[1] == "l"):
                moveMouse(590, 100)
                time.sleep(0.25)
                pyautogui.click()
            if(dir[1] == "right" or dir[1] == "r"):
                moveMouse(710, 100)
                time.sleep(0.25)
                pyautogui.click()

        
        #irc right click inventory spot
        elif "irc" in line: 
            #perform right click on coordinates given
            coords = line.split(' ')[1].strip()
            num = int(re.split("[^\d]", coords)[1])
            if coords[0] in ['a', 'b', 'c', 'd'] and num < 8 and num >= 0:
                leftClickInv(coords[0], num, True)

        elif "esc"==line or "cancel"==line or "escape"==line:
            pyautogui.keyDown("Escape")
            time.sleep(0.25) 
            pyautogui.keyUp("Escape")
        
        elif "qu"==line or line.startswith("qu "):
            leftClickInv('a', 1)
        
        
        elif "lc"==line or "click"==line: 
            pyautogui.click()
        elif "rc"==line or "right click"==line: 
            pyautogui.click(button="right")

        #lc a12 - left click on grid
        elif "lc" in line: 
            #perform left click on coordinates given
            coords = line.split(' ')[1].strip()
            num = int(re.split("[^\d]", coords)[1])
            if coords[0] in alphabetToNums and num < 14 and num >= 0:
                leftClickMain(coords[0], num)
        
        #rc a12 - right click on grid
        elif "rc" in line: 
            #perform right click on coordinates given
            coords = line.split(' ')[1].strip()
            num = int(re.split("[^\d]", coords)[1])
            if coords[0] in alphabetToNums and num < 14 and num >= 0:
                leftClickMain(coords[0], num, True)
        
        #reset, reset camera, compass - Reset camera
        elif line=="stop":
            moveMouse(260, 210)
            pyautogui.click()
        
        #reset, reset camera, compass - Reset camera
        elif line=="reset" or line=="reset camera" or line=="compass":
            clickCompass()
        #run, walk - run
        elif line=="run" or line=="walk" or line=="sprint":
            clickRun()
        #sa, special, special attack - special attack
        elif line=="sa" or line=="special" or line=="special attack":
            clickSpecial()
        #pray, prayer - prayer on
        elif line=="pray" or line=="prayer":
            clickPrayer()
        
        elif line.startswith("say: "):
            pyautogui.write(line.split("say: ")[1], interval=0.1)
            pyautogui.keyDown("Enter")
            time.sleep(0.25) 
            pyautogui.keyUp("Enter")
        
        #direction dur(optional)
        elif line.startswith("left") or line.startswith("up") or line.startswith("right") or line.startswith("down"):
            dur = line.split(' ')
            if len(dur) == 2:
                if(int(dur[1]) <= 3000):
                    arrowKey(dur[0], int(dur[1]))
            else:
                arrowKey(line)
        
        #move mouse x y
        elif line.startswith("move mouse to"):
            dur = line.split(' ')
            if len(dur) == 5:
                if(int(dur[3]) <= MAXX and int(dur[4])*-1 <= MAXY):
                    moveMouse(int(dur[3]), int(dur[4]))
            else:
                arrowKey(line)
        
        elif line.startswith("center mouse"):
            moveMouse(260, 210)
        
        #move mouse x y
        elif line.startswith("move mouse"):
            dur = line.split(' ')
            if len(dur) == 4:
                if(int(dur[2]) <= 400 and int(dur[3]) <= 400):
                    moveMouseRelative(int(dur[2]), int(dur[3])*-1)
            else:
                arrowKey(line)
        
        #click on a certain menu item
        elif line.startswith("menu") or line.startswith("m"):
            dur = line.split(' ')
            if len(dur) == 2:
                if(int(dur[1]) <= 6):
                    menuClick(int(dur[1]))
        elif line=="zoom in" or line=="zoom out":
            moveMouse(260, 210)
            zoom(line.split(' ')[1])
        elif line=="scroll up"or line=="scroll down":
            zoom(line.split(' ')[1])

        elif line == "space" or line == "spacebar": 
            keyPress("space")
        
        elif line == "combat" or line == "style" or line == "attack style": 
            keyPress("F1")
        
        elif line == "stats" or line == "exp": 
            keyPress("F2")
        
        elif line == "chat channel" or line == "minigame" or line == "clan" or line == "group": 
            keyPress("F10")
        
        elif line == "quests":
            keyPress("F3")
        
        
        elif line == "i" or line == "inv" or line == "inventory": 
            keyPress("F4")
        
        elif line == "gear" or line == "equip" or line == "equipment": 
            keyPress("F5")

        elif line == "prayers": 
            keyPress("F6")
        
        elif line == "spells" or line == "spellbook": 
            keyPress("F7")
        
        elif line == "emote" or line == "emotes": 
            keyPress("F11")
        
        elif line == "music" or line == "song" or line =="songs": 
            keyPress("F12")

        if line.isnumeric():
            try:
                num = re.split("[^\d]", line)[0][0]
                if(int(num)):
                    keyPress(num)
            except:
                return
        try:
            first_char = line[0]
            if(first_char in alphabetToNums and line[1].isnumeric()):
                leftClickMain(line[0], int(re.split("[^\d]", line)[1]))
        except:
            return
    elif tester[0] != -1:
        if line == "login":
            login()
    elif bankPin[0] != -1:
        pyautogui.keyDown("Escape")
        time.sleep(0.25) 
        pyautogui.keyUp("Escape")
    


    

    



#Have a function for each of these commands

#Have a function for each functionality commands will call


#Move mouse, click, right click, press F1-F9, numpad 0-9, arrow keys

alphabetToNums = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']




startingMainSquareX = 20
startingMainSquareY = 40
mainSquareWidth = 25.5
mainSquareHeight = 25.5

invStartingX = 575
invStartingY = 250
invSquareWidth = 45
invSquareHeight = 37

compassX = 565
compassY = 48

prayerX = 560
prayerY = 117

runX = 570
runY = 150

specialX = 600
specialY = 175

def leftClickMain(letter, number, right=False):
    xCoord = startingMainSquareX + (alphabetToNums.index(letter) * mainSquareWidth)
    yCoord = startingMainSquareY + (number-1) * mainSquareHeight
    if right: 
        moveMouse(xCoord, yCoord)
        pyautogui.click(button="right")
    else: 
        moveMouse(xCoord, yCoord)
        time.sleep(0.25)
        pyautogui.click()

def leftClickInv(letter, number, right=False):
    xCoord = invStartingX + (alphabetToNums.index(letter) * invSquareWidth)
    yCoord = invStartingY + (number-1) * invSquareHeight

    if right: 
        moveMouse(xCoord, yCoord)
        pyautogui.click(button="right")
    else:
        moveMouse(xCoord, yCoord)
        time.sleep(0.25)
        pyautogui.click()

def dropItem(letter, number):
    xCoord = invStartingX + (alphabetToNums.index(letter) * invSquareWidth)
    yCoord = invStartingY + (number-1) * invSquareHeight

    moveMouse(xCoord, yCoord)
    pyautogui.keyDown("shift")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyUp("shift")

def login():
    isOnMainScreen = imagesearch("loginscreen.PNG", 0.8)
    if isOnMainScreen[0] != -1:
        isOnDC = imagesearch("disconnectscreen.PNG", 0.8)
        if isOnDC[0] != -1:
            moveMouse(430, 320)
            pyautogui.click()
        pyautogui.keyDown("enter")
        time.sleep(0.1)
        pyautogui.keyUp("enter")
        time.sleep(0.1)
        pyautogui.write(password, interval=0.1)
        pyautogui.keyDown("Enter")
        time.sleep(0.25) 
        pyautogui.keyUp("Enter")

        time.sleep(10)
        moveMouse(430, 320)
        time.sleep(0.25)
        pyautogui.click()

    

def menuClick(number):
    moveMouseRelative(0, 20)
    moveMouseRelative(0, 15.8*(number-1))

    pyautogui.click()
    

def clickCompass(): 
    pyautogui.click(compassX, compassY)

def clickPrayer(): 
    pyautogui.click(prayerX, prayerY)

def clickRun(): 
    pyautogui.click(runX, runY)

def clickSpecial(): 
    pyautogui.click(specialX, specialY)

def arrowKey(key, dur=250):
    pyautogui.keyDown(key)
    time.sleep(dur/1000)
    pyautogui.keyUp(key)

def zoom(dir, tick=500):
    if dir=="up" or dir=="in":
        pyautogui.scroll(tick)
        print(tick)
    elif dir=="down" or dir=="out":
        pyautogui.scroll(-tick)

def keyPress(key):
    pyautogui.keyDown(key)
    time.sleep(0.25)
    pyautogui.keyUp(key)



MAXX = 760
MAXY = 480

def moveMouse(x, y):
    if(x < MAXX and y < MAXY and y > 25):
        pyautogui.moveTo(x, y)

def moveMouseRelative(x, y):
    if(pyautogui.position()[0] + x < MAXX and pyautogui.position()[1] + y < MAXY and pyautogui.position()[1] + y > 25):
        pyautogui.move(x, y)




# while True:
#     print(pyautogui.position())

# time.sleep(4)

main()



# login()

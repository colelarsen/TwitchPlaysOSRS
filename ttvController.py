import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
from config import *

import osrsController as osrs


class winSize:
    def __init__(self):
        self.xMax = 760
        self.yMax = 480
        self.xMin = 0 
        self.yMin = 25

    # Ensure target is within window
    def check_x(self,x):
        return x < self.xMax and x > self.xMin
    def check_y(self,y):
        return y < self.yMax and y > self.yMin

    # Return mouse positions
    def mouse_x_pos(self):
        return pyautogui.position()[0]
    def mouse_y_pos(self):
        return pyautogui.position()[1]
    
    # Mouse moving functions, one absolute the other relative to curr pos
    def moveMouse(self, x, y):
        if self.check_x(x) and self.check_y(y):
            pyautogui.moveTo(x, y)
    def moveMouseRelative(self, x, y):
        if self.check_x(x + self.mouse_x_pos()) and self.check_y(y + self.mouse_y_pos()):
            pyautogui.moveTo(x, y)


def arrowKey(self, key, dur=250):
    pyautogui.keyDown(key)
    time.sleep(dur/1000)
    pyautogui.keyUp(key)
def zoom(self, dir, tick=500):
    if dir=="up" or dir=="in":
        pyautogui.scroll(tick)
        print(tick)
    elif dir=="down" or dir=="out":
        pyautogui.scroll(-tick)
def keyPress(self, key):
    pyautogui.keyDown(key)
    time.sleep(0.1)
    pyautogui.keyUp(key)


class ttvController:
    def __init__(self):
        self.win = winSize()
        self.osrs = osrs(self.win)



    def readChat(self, resp):
        resp = resp.rstrip().split('\r\n')
        line = random.choice(resp)
        if "PRIVMSG" in line:
            user = line.split(':')[1].split('!')[0]
            msg = line.split(':', maxsplit=2)[2]
            line = user + ": " + msg
            self.parseChat(msg)


    def parseChat(self, lineRaw):  

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
                    self.osrs.ClickInv(coords[0], num)
            elif line[0]=='i' and line[1] in ['a', 'b', 'c', 'd'] and line[2].isnumeric():
                num = int(line[2])
                if num < 8 and num >= 0:
                    self.osrs.ClickInv(line[1], num)

            elif line.startswith("drop "): 
                #perform left click on coordinates given
                coords = line.split(' ')[1].strip()
                num = int(re.split("[^\d]", coords)[1])
                if coords[0] in ['a', 'b', 'c', 'd'] and num < 8 and num >= 0:
                    self.osrs.dropItem(coords[0], num)

            elif line.startswith("mm "): 
                dir = line.split(' ')
                if(dir[1] == "top" or dir[1] == "t"):
                    self.win.moveMouse(650, 40)
                    time.sleep(0.25)
                    pyautogui.click()
                if(dir[1] == "bottom" or dir[1] == "bot" or dir[1] == "b"):
                    self.win.moveMouse(650, 160)
                    time.sleep(0.25)
                    pyautogui.click()
                if(dir[1] == "left" or dir[1] == "l"):
                    self.win.moveMouse(590, 100)
                    time.sleep(0.25)
                    pyautogui.click()
                if(dir[1] == "right" or dir[1] == "r"):
                    self.win.moveMouse(710, 100)
                    time.sleep(0.25)
                    pyautogui.click()

            
            #irc right click inventory spot
            elif "irc" in line: 
                #perform right click on coordinates given
                coords = line.split(' ')[1].strip()
                num = int(re.split("[^\d]", coords)[1])
                if coords[0] in ['a', 'b', 'c', 'd'] and num < 8 and num >= 0:
                    self.osrs.ClickInv(coords[0], num, True)

            elif "esc"==line or "cancel"==line or "escape"==line:
                pyautogui.keyDown("Escape")
                time.sleep(0.25) 
                pyautogui.keyUp("Escape")
            
            elif "qu"==line or line.startswith("qu "):
                self.osrs.ClickInv('a', 1)
            
            
            elif "lc"==line or "click"==line: 
                pyautogui.click()
            elif "rc"==line or "right click"==line: 
                pyautogui.click(button="right")

            #lc a12 - left click on grid
            elif "lc" in line: 
                #perform left click on coordinates given
                coords = line.split(' ')[1].strip()
                letter = coords[0]
                num = int(re.split("[^\d]", coords)[1])
                if osrs.checkMainCoord(letter, num):
                    self.osrs.ClickMain(letter, num)
            
            #rc a12 - right click on grid
            elif "rc" in line: 
                #perform right click on coordinates given
                coords = line.split(' ')[1].strip()
                letter = coords[0]
                num = int(re.split("[^\d]", coords)[1])
                if osrs.checkMainCoord(letter, num):
                    self.osrs.ClickMain(letter, num, True)
            
            #reset, reset camera, compass - Reset camera
            elif line=="stop":
                self.win.moveMouse(260, 210)
                pyautogui.click()
            
            #reset, reset camera, compass - Reset camera
            elif line=="reset" or line=="reset camera" or line=="compass":
                self.osrs.uiButtons.clickCompass()
            #run, walk - run
            elif line=="run" or line=="walk" or line=="sprint":
                self.osrs.uiButtons.clickRun()
            #sa, special, special attack - special attack
            elif line=="sa" or line=="special" or line=="special attack":
                self.osrs.uiButtons.clickSpecial()
            #pray, prayer - prayer on
            elif line=="pray" or line=="prayer":
                self.osrs.uiButtons.clickPrayer()
            
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
                    if(int(dur[3]) <= self.win.xMax and int(dur[4])*-1 <= self.win.yMax):
                        self.win.moveMouse(int(dur[3]), int(dur[4]))
                else:
                    arrowKey(line)
            
            elif line.startswith("center mouse"):
                self.win.moveMouse(260, 210)
            
            #move mouse x y
            elif line.startswith("move mouse"):
                dur = line.split(' ')
                if len(dur) == 4:
                    if(int(dur[2]) <= 400 and int(dur[3]) <= 400):
                        self.win.moveMouseRelative(int(dur[2]), int(dur[3])*-1)
                else:
                    arrowKey(line)
            
            #click on a certain menu item
            elif line.startswith("menu") or line.startswith("m"):
                dur = line.split(' ')
                if len(dur) == 2:
                    if(int(dur[1]) <= 6):
                        self.osrs.menuClick(int(dur[1]))
            elif line=="zoom in" or line=="zoom out":
                self.win.moveMouse(260, 210)
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
                if(first_char in self.osrs.main.cols and line[1].isnumeric()):
                    self.osrs.ClickMain(line[0], int(re.split("[^\d]", line)[1]))
            except:
                return
        elif tester[0] != -1:
            if line == "login":
                self.osrs.login()
        elif bankPin[0] != -1:
            pyautogui.keyDown("Escape")
            time.sleep(0.25) 
            pyautogui.keyUp("Escape")

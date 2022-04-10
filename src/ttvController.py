import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
import commandValidation as validation
from config import *
import utility

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
    
    #TODO: add a click function here that moves the mouse
    
    # Mouse moving functions, one absolute the other relative to curr pos
    def moveMouse(self, coords):
        x = coords[0]
        y = coords[1]
        if self.check_x(x) and self.check_y(y):
            pyautogui.moveTo(x, y)
    def moveMouseRelative(self, coords):
        x = coords[0]
        y = coords[1]
        if self.check_x(x + self.mouse_x_pos()) and self.check_y(y + self.mouse_y_pos()):
            pyautogui.moveTo(x, y)


class TtvController:
    def __init__(self):
        self.win = winSize()
        self.osrs = osrs.osrsController(self.win)
        self.validation = validation.ValidationController(self.osrs)

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

        # tester = imagesearch("Images/loginscreen.PNG", 0.8)
        # bankPin = imagesearch("Images/bankPin.PNG", 0.8)
        # if tester[0] == -1 and bankPin[0] == -1:
        if True:
        
            num = utility.getFirstNumber(line)
            #Check if the input line should left click on inv
            if self.validation.validInvLClick(line): 
                self.osrs.clickInv(line[0], num)
            
            #[a-t][1-13] - left click on grid
            elif self.validation.validMainLClick(line):
                self.osrs.clickMain(line[0], num)

            elif self.validation.validDrop(line):
                coords = line.split(' ')[1].strip()
                self.osrs.dropItem(coords[0], num)
            
            #right click inventory spot
            elif self.validation.validInvRClick(line): 
                self.osrs.clickInv(line[1], num, True)
            
            #right click main
            elif self.validation.validMainRClick(line): 
                self.osrs.clickMain(line[1], num, True)

            elif line.startswith("mm ") or line.startswith("m ") or line.startswith("map "): 
                dir = line.split(' ')
                if(dir[1] in ["top", "t"]):
                    self.win.moveMouse(650, 40)
                    pyautogui.click()
                if dir[1] in ["bottom", "b", "bot", "down", "d"]:
                    self.win.moveMouse(650, 160)
                    pyautogui.click()
                if(dir[1] in ["left", "l"]):
                    self.win.moveMouse(590, 100)
                    pyautogui.click()
                if(dir[1] in ["right", "r"]):
                    self.win.moveMouse(710, 100)
                    pyautogui.click()
                #TODO add diagonal options

            elif line in ["escape", "cancel", "quit", "exit"]: 
                pyautogui.keyDown("Escape")
                time.sleep(0.25) 
                pyautogui.keyUp("Escape")
            
            elif "qu"==line or line.startswith("qu "):
                self.osrs.clickInv('a', 1)
            
            
            elif line in ["c", "lc", "click"]: 
                pyautogui.click()
            elif line in ["r", "rc", "right click"]: 
                pyautogui.click(button="right")

            
            #reset, reset camera, compass - Reset camera
            elif line=="stop":
                self.win.moveMouse(260, 210)
                pyautogui.click()
            
            #reset, reset camera, compass - Reset camera
            elif line in ["reset", "reset camera", "compass"]:
                self.osrs.uiButtons.clickCompass()
            #run, walk - run
            elif line in ["run", "walk", "sprint"]:
                self.osrs.uiButtons.clickRun()
            #sa, special, special attack - special attack
            elif line in ["sa", "special", "special attack"]:
                self.osrs.uiButtons.clickSpecial()
            #pray, prayer - prayer on
            elif line in ["pray", "prayer"]:
                self.osrs.uiButtons.clickPrayer()
            
            elif line.startswith("say: "):
                pyautogui.write(line.split("say: ")[1], interval=0.1)
                pyautogui.keyDown("Enter")
                time.sleep(0.1) 
                pyautogui.keyUp("Enter")
            
            #direction dur(optional)
            elif line.startswith("cam ") or line.startswith("c "):
                lineWords = line.split(' ')
                dir = lineWords[1]
                
                if dir in ["left", "right", "down", "up"]:
                    if len(lineWords) == 2:
                        dur = lineWords[2]
                        if(int(dur[1]) <= 3000):
                            osrs.arrowKey(dir, int(dur[1]))
                    else:
                        osrs.arrowKey(dir)
            
            #move mouse x y
            elif line.startswith("move mouse to"):
                dur = line.split(' ')
                if len(dur) == 5:
                    if(int(dur[3]) <= self.win.xMax and int(dur[4])*-1 <= self.win.yMax):
                        self.win.moveMouse(int(dur[3]), int(dur[4]))
                else:
                    osrs.arrowKey(line)
            
            elif line.startswith("center mouse"):
                self.win.moveMouse(260, 210)
            
            #move mouse x y
            elif line.startswith("move mouse"):
                dur = line.split(' ')
                if len(dur) == 4:
                    if(int(dur[2]) <= 400 and int(dur[3]) <= 400):
                        self.win.moveMouseRelative(int(dur[2]), int(dur[3])*-1)
                else:
                    osrs.arrowKey(line)
            
            #click on a certain menu item
            elif line.startswith("menu") or line.startswith("m"):
                dur = line.split(' ')
                if len(dur) == 2:
                    if(int(dur[1]) <= 6):
                        self.osrs.menuClick(int(dur[1]))
            elif line=="zoom in" or line=="zoom out":
                self.win.moveMouse(260, 210)
                osrs.zoom(line.split(' ')[1])
            elif line=="scroll up"or line=="scroll down":
                osrs.zoom(line.split(' ')[1])

            elif line == "space" or line == "spacebar": 
                osrs.keyPress("space")
            
            elif line == "combat" or line == "style" or line == "attack style": 
                osrs.keyPress("F1")
            
            elif line == "stats" or line == "exp": 
                osrs.keyPress("F2")
            
            elif line == "chat channel" or line == "minigame" or line == "clan" or line == "group": 
                osrs.keyPress("F10")
            
            elif line == "quests":
                osrs.keyPress("F3")
            
            
            elif line == "i" or line == "inv" or line == "inventory": 
                osrs.keyPress("F4")
            
            elif line == "gear" or line == "equip" or line == "equipment": 
                osrs.keyPress("F5")

            elif line == "prayers": 
                osrs.keyPress("F6")
            
            elif line == "spells" or line == "spellbook": 
                osrs.keyPress("F7")
            
            elif line == "emote" or line == "emotes": 
                osrs.keyPress("F11")
            
            elif line == "music" or line == "song" or line =="songs": 
                osrs.keyPress("F12")

            if line.isnumeric():
                try:
                    num = re.split("[^\d]", line)[0][0]
                    if(int(num)):
                        osrs.keyPress(num)
                except:
                    return
            try:
                first_char = line[0]
                if(first_char in self.osrs.main.cols and line[1].isnumeric()):
                    self.osrs.clickMain(line[0], int(re.split("[^\d]", line)[1]))
            except:
                return
        # elif tester[0] != -1:
        #     if line == "login":
        #         self.osrs.login()
        # elif bankPin[0] != -1:
        #     pyautogui.keyDown("Escape")
        #     time.sleep(0.25) 
        #     pyautogui.keyUp("Escape")
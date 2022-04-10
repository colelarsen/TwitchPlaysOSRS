import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
import commandValidation as validation
from config import *
import utility
import threading

import osrsController as osrs


class winSize:
    def __init__(self):
        self.xMax = 760
        self.yMax = 480
        self.xMin = 0 
        self.yMin = 25

        self.xCenter = (self.xMax - self.xMin) / 2
        self.yCenter = (self.yMax - self.yMin) / 2

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
        self.validation = validation.ValidationController(self.osrs, self.win)

    def readChat(self, resp):
        resp = resp.rstrip().split('\r\n')
        try:
            for i in resp:
                line = random.choice(resp)
                if "PRIVMSG" in line:
                    user = line.split(':')[1].split('!')[0]
                    msg = line.split(':', maxsplit=2)[2]
                    line = user + ": " + msg
                    wasValid = self.parseChat(msg)
                    if wasValid:
                        print(line + ": was valid")
                        break
        except Exception as e: 
                print(e)


    def parseChat(self, lineRaw):  
        line = lineRaw.lower()

        wasValidLine = True

        #Run all validation rules against this line... this is faster than doing image recogniztion everytime for bad input
        if self.validation.isValidInput(line):

            isOnLoginScreen = imagesearch("Images/loginscreen.PNG", 0.8)[0] != -1
            isOnBankPinScreen = imagesearch("Images/bankPin.PNG", 0.8)[0] != -1
            
            if isOnBankPinScreen:
                pyautogui.keyDown("Escape")
                time.sleep(0.25) 
                pyautogui.keyUp("Escape")
            elif isOnLoginScreen and line == "login":
                self.osrs.login()
            

            elif not isOnLoginScreen and not isOnBankPinScreen:
            # elif True: #uncomment this when you want to do some debugging locally without checking for bank shit
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
                
                #right click main
                elif self.validation.validDrag(line): 
                    lineWords = line.split(' ')
                    firstBar = lineWords[1]
                    secondBar = lineWords[2]
                    num1 = utility.getFirstNumber(firstBar)
                    num2 = utility.getFirstNumber(secondBar)
                    self.osrs.dragItem(firstBar[0], num1, secondBar[0], num2)

                elif self.validation.validMapMove(line): 
                    dir = line.split(' ')
                    if(dir[1] in ["top", "t"]):
                        self.win.moveMouse((650, 40))
                        pyautogui.click()
                    if dir[1] in ["bottom", "b", "bot", "down", "d"]:
                        self.win.moveMouse((650, 160))
                        pyautogui.click()
                    if(dir[1] in ["left", "l"]):
                        self.win.moveMouse((590, 100))
                        pyautogui.click()
                    if(dir[1] in ["right", "r"]):
                        self.win.moveMouse((710, 100))
                        pyautogui.click()

                    if(dir[1] in ["top right", "tr", "ur", "up right"]):
                        self.win.moveMouse((710, 60))
                        pyautogui.click()
                    if(dir[1] in ["top left", "tl", "ul", "up left"]):
                        self.win.moveMouse((600, 60))
                        pyautogui.click()
                    if(dir[1] in ["bot right", "bottom right", "br", "dr", "down right"]):
                        self.win.moveMouse((710, 150))
                        pyautogui.click()
                    if(dir[1] in ["bot left", "bottom left", "bl", "dl", "down left"]):
                        self.win.moveMouse((600, 150))
                        pyautogui.click()
                    #TODO add diagonal options

                elif self.validation.validEscape(line):
                    pyautogui.keyDown("Escape")
                    time.sleep(0.25) 
                    pyautogui.keyUp("Escape")
                
                elif self.validation.validQuickUse(line):
                    self.osrs.clickInv('a', 1)
                
                
                elif self.validation.validClick(line): 
                    pyautogui.click()
                elif self.validation.validRClick(line): 
                    pyautogui.click(button="right")

                
                #reset, reset camera, compass - Reset camera
                elif self.validation.validStop(line):
                    self.win.moveMouse(260, 210)
                    pyautogui.click()
                
                #reset, reset camera, compass - Reset camera
                elif self.validation.validResetCam(line):
                    self.osrs.uiButtons.clickCompass()

                #run, walk - run
                elif self.validation.validRun(line):
                    self.osrs.uiButtons.clickRun()
                #sa, special, special attack - special attack
                elif self.validation.validSpecialAttack(line):
                    self.osrs.uiButtons.clickSpecial()
                #pray, prayer - prayer on
                elif self.validation.validPrayer(line):
                    self.osrs.uiButtons.clickPrayer()
                
                elif self.validation.validSay(line):
                    x = threading.Thread(target=self.osrs.typeText, args=(line,))
                    x.start()
                    
                
                #direction dur(optional)
                elif self.validation.validCam(line):
                    lineWords = line.split(' ')
                    dir = lineWords[1]
                    if len(lineWords) == 3:
                        self.osrs.arrowKey(dir,num)
                    else:
                        self.osrs.arrowKey(dir)
                
                #move mouse x y
                elif self.validation.validMouseMoveTo(line):
                    dur = line.split(' ')
                    self.win.moveMouse(int(dur[3]), int(dur[4]))
                
                elif self.validation.validCenterMouse(line):
                    self.win.moveMouse(260, 210)
                
                #move mouse x y
                elif self.validation.validMouseMove(line):
                    dur = line.split(' ')
                    self.win.moveMouseRelative(int(dur[2]), int(dur[3])*-1)
                
                #click on a certain menu item
                elif self.validation.validMenu(line):
                    if(num <= 9):
                        self.osrs.menuClick(num)

                elif self.validation.validZoom(line):
                    self.win.moveMouse(260, 210)
                    self.osrs.zoom(line.split(' ')[1])

                elif self.validation.validScroll(line):
                    self.osrs.zoom(line.split(' ')[1])

                elif self.validation.validSpace(line): 
                    lineWords = line.split(' ')
                    if len(lineWords) > 1 and lineWords[1].isnumeric():
                        number = int(lineWords[1])
                        if number <= 3000:
                            self.osrs.keyPress("space", number)
                    else:
                        self.osrs.keyPress("space")



                elif self.validation.validCombat(line): 
                    osrs.keyPress("F1")
                
                elif self.validation.validStats(line): 
                    osrs.keyPress("F2")
                
                elif self.validation.validGroup(line): 
                    osrs.keyPress("F10")
                
                elif self.validation.validQuests(line): 
                    osrs.keyPress("F3")
                
                elif self.validation.validInv(line): 
                    osrs.keyPress("F4")
                
                elif self.validation.validGear(line):
                    osrs.keyPress("F5")

                elif self.validation.validPrayers(line): 
                    osrs.keyPress("F6")
                
                elif self.validation.validSpells(line): 
                    osrs.keyPress("F7")
                
                elif self.validation.validEmotes(line): 
                    osrs.keyPress("F11")
                
                elif self.validation.validMusic(line):
                    osrs.keyPress("F12")

                #If the entire line is a number get the first number
                elif self.validation.validNumerical():
                    #GET THE FIRST DIGIT of the first line
                    firstNum = re.split("[^\d]", line)[0][0]
                    if(int(firstNum)):
                        self.osrs.keyPress(firstNum)
                else:
                    wasValidLine = False
        else:
            wasValidLine = False
        return wasValidLine
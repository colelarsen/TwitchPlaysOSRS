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

        self.screenshot = self.screenshotArea()

        self.xCenter = (self.xMax - self.xMin) / 2
        self.yCenter = (self.yMax - self.yMin) / 2

    class screenshotArea:
        xMin = 0
        yMin = 0
        xMax = 770
        yMax = 530

        def region(self):
            return self.xMin, self.yMin, self.xMax, self.yMax

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
            pyautogui.moveTo(x + self.mouse_x_pos(), y + self.mouse_y_pos())


class TtvController:
    def __init__(self):
        self.win = winSize()
        self.osrs = osrs.osrsController(self.win)
        self.validation = validation.ValidationController(self.osrs, self.win)
        self.isOnLoginScreen = False 
        self.isOnBankSettingsScreen = False
        self.screen_check()
        self.checkBankPin()

    def screen_check(self):
        print('checking Screen')
        im = region_grabber(self.win.screenshot.region())
        self.checkLoginScreen(im)
        self.checkBankSettings(im)


    def checkLoginScreen(self, im=None):
        self.isOnLoginScreen = imagesearcharea("Images/loginscreen.PNG", *self.win.screenshot.region(), 0.8, im)[0] != -1

    def checkBankSettings(self, im=None):
        self.isOnBankSettingsScreen = imagesearcharea("Images/bankPinSettings.PNG", *self.win.screenshot.region(), 0.8, im)[0] != -1

    def checkBankPin(self, im=None):
        self.isOnBankPinScreen = imagesearcharea("Images/bankPinEntry.PNG", *self.win.screenshot.region(), 0.8, im)[0] != -1

    def readChat(self, messages):
        try:
            for i in messages:
                message = random.choice(messages)
                wasValid = self.parseChat(message)
                line = message.command
                if wasValid:
                    print(line + ": was valid")
                    break
        except Exception as e: 
                print(e)


    def parseChat(self, messageObj):  

        line = messageObj.command
        wasValidLine = True

        #Run all validation rules against this line... this is faster than doing image recogniztion everytime for bad input
        if self.validation.isValidInput(line):

            if self.isOnLoginScreen and (line == "login" or line == "!login"):
                self.osrs.login()
                self.checkLoginScreen()
            

            elif not self.isOnLoginScreen and not self.isOnBankSettingsScreen:
            # elif True: #uncomment this when you want to do some debugging locally without checking for bank shit
                num = utility.getFirstNumber(line)
                secondNum = utility.getSecondNumber(line)

                #Check if the input line should left click on inv
                if self.validation.validInvLClick(line): 
                    self.osrs.inv.clickPos(line[0], num)
                
                #[a-t][1-13] - left click on grid
                elif self.validation.validMainLClick(line):
                    self.osrs.main.clickPos(line[0], num)

                elif self.validation.validDrop(line):
                    coords = ""
                    if(not line.startswith("drop") and not  line.startswith("d ")):
                        coords = line.split('d')[1].strip()
                        coords = coords.split(' ')[0].strip()
                    else:
                        coords = line.split(' ')[1].strip()

                    self.osrs.inv.dropItem(coords[0], num)
                
                #right click inventory spot
                elif self.validation.validInvRClick(line): 
                    self.osrs.inv.clickPos(line[1], num, True)
                
                #right click main
                elif self.validation.validMainRClick(line): 
                    self.osrs.main.clickPos(line[1], num, True)
                
                #right click main
                elif self.validation.validDrag(line): 
                    lineWords = line.split(' ')
                    firstBar = lineWords[1]
                    secondBar = lineWords[2]
                    num1 = utility.getFirstNumber(firstBar)
                    num2 = utility.getFirstNumber(secondBar)
                    self.osrs.inv.dragItem(firstBar[0], num1, secondBar[0], num2)

                elif self.validation.validMapMove(line): # Need to add scaling to regex
                    dist = 80
                    if num < 100 and num > 0:
                        dist = num
                    dir = line.split(' ')[1]

                    anglemod = .7
                    
                    if(dir in ["top", "t", "up", "u"]):
                        self.osrs.map.clickMap('u', dist)
                    if dir in ["bottom", "b", "bot", "down", "d"]:
                        self.osrs.map.clickMap('d', dist)
                    if(dir in ["left", "l"]):
                        self.osrs.map.clickMap('l', dist)
                    if(dir in ["right", "r"]):
                        self.osrs.map.clickMap( 'r', dist)
                    if(dir in ["top right", "tr", "ur", "up right"]):
                        self.osrs.map.clickMap('ur', dist * anglemod)
                    if(dir in ["top left", "tl", "ul", "up left"]):
                        self.osrs.map.clickMap('ul', dist * anglemod)
                    if(dir in ["bot right", "bottom right", "br", "dr", "down right"]):
                        self.osrs.map.clickMap('dr', dist * anglemod)
                    if(dir in ["bot left", "bottom left", "bl", "dl", "down left"]):
                        self.osrs.map.clickMap('dl', dist * anglemod)

                elif self.validation.validEscape(line):
                    pyautogui.keyDown("Escape")
                    time.sleep(0.1) 
                    pyautogui.keyUp("Escape")

                elif self.validation.validQuests(line): 
                    self.osrs.keyPress("F3")
                
                elif self.validation.validQuickUse(line):
                    self.osrs.inv.clickPos('w', 1)
                    line = re.search("^(qu)( [w-z][1-7])?", line)
                    # if line.group() != 'qu':
                    #     col = line.group().split(' ')[1]
                    #     print(col)
                    #     self.osrs.inv.clickPos(col[0],num)
                
                
                elif self.validation.validClick(line): 
                    pyautogui.click()
                elif self.validation.validRClick(line): 
                    pyautogui.click(button="right")

                
                #reset, reset camera, compass - Reset camera
                elif self.validation.validStop(line):
                    self.win.moveMouse((260, 210))
                    pyautogui.click()
                
                #reset, reset camera, compass - Reset camera
                elif self.validation.validResetCam(line):
                    self.osrs.buttons.clickCompass()

                #run, walk - run
                elif self.validation.validRun(line):
                    if not self.osrs.buttons.checkRun():
                        print('sprint on')
                        self.osrs.buttons.clickRun()

                elif self.validation.validWalk(line):
                    if self.osrs.buttons.checkRun():
                        print('sprint off')
                        self.osrs.buttons.clickRun()
                
                #sa, special, special attack - special attack
                elif self.validation.validSpecialAttack(line):
                    self.osrs.buttons.clickSpecial()
                #pray, prayer - prayer on
                elif self.validation.validPrayer(line):
                    self.osrs.buttons.clickPrayer()
                
                elif self.validation.validSay(line):
                    x = threading.Thread(target=self.osrs.typeText, args=(line,True))
                    x.start()

                elif self.validation.validType(line):
                    x = threading.Thread(target=self.osrs.typeText, args=(line,))
                    x.start()

                elif self.validation.validBankDeposit(line):
                    lineWords = line.split(' ')
                    action = lineWords[1]
                    if action in ['inv','inventory']:
                        self.osrs.bank.depositInv() 
                    elif action in ['equip','equipment']:
                        self.osrs.bank.depositEquip()

                elif self.validation.validBankQuantity(line):
                    lineWords = line.split(' ')
                    quantity = lineWords[1]
                    self.osrs.bank.changeQuantity(quantity.split('q')[1])

                elif self.validation.validBankOpen(line):
                    self.checkBankPin()
                    if self.isOnBankPinScreen:
                        lineWords = line.split(' ')
                        pin = lineWords[2]
                        self.osrs.openBank(pin)
                

                #direction dur(optional)
                elif self.validation.validCam(line):
                    lineWords = line.split(' ')
                    dir = lineWords[1]
                    if len(lineWords) == 3:
                        x = threading.Thread(target=self.osrs.arrowKey, args=(dir,num,))
                        x.start()
                    else:
                        x = threading.Thread(target=self.osrs.arrowKey, args=(dir,))
                        x.start()

                #Quarter turn = 815

                #full turn = 3620

                elif self.validation.validAngleCam(line):
                    qt = 815
                    lineWords = line.split(' ')
                    dir = lineWords[1]
                    if dir == 'qtr':
                        x = threading.Thread(target=self.osrs.arrowKey, args=('right',qt,))
                        x.start()
                    elif dir == 'qtl':
                        x = threading.Thread(target=self.osrs.arrowKey, args=('left',qt,))
                        x.start()



                elif self.validation.validDir(line):
                    lineWords = line.split(' ')
                    dir = lineWords[0]
                    
                    if len(lineWords) > 1 and num in range(1,8):
                        print('first')
                        self.osrs.main.move_dir(dir,num)
                    else:
                        self.osrs.main.move_dir(dir)


                elif self.validation.validCenterMouse(line):
                    self.win.moveMouse((260, 210))
                
                
                #click on a certain menu item
                elif self.validation.validMenu(line):
                    if(num <= 9):
                        self.osrs.menuClick(num)

                elif self.validation.validZoom(line) or self.validation.validScroll(line): # Identical save to mouse movement, merge rest     
                    lineWords = line.split(' ')
                    dir = lineWords[1]
                    if num != None:
                        self.osrs.zoom(dir, num * 500)

                    else:
                        self.osrs.zoom(dir)

                # elif self.validation.validScroll(line):
                #     lineWords = line.split(' ')
                #     dir = lineWords[1]
                #     if num != None:
                #         self.osrs.zoom(dir, num * 500)
                #     else:
                #         self.osrs.zoom(dir)

                elif self.validation.validSpace(line): 
                    lineWords = line.split(' ')
                    if len(lineWords) > 1 and lineWords[1].isnumeric():
                        number = int(lineWords[1])
                        if number <= 10000:
                            x = threading.Thread(target=self.osrs.keyPress, args=('space',number,))
                            x.start()
                    else:
                        self.osrs.keyPress("space")



                elif self.validation.validCombat(line): 
                    self.osrs.keyPress("F1")
                
                elif self.validation.validStats(line): 
                    self.osrs.keyPress("F2")
                
                # Former location of quest button, our dummy asses moved it higher in cascade instead of coding properly
                
                elif self.validation.validInv(line): 
                    self.osrs.keyPress("F4")
                
                elif self.validation.validGear(line):
                    self.osrs.keyPress("F5")

                elif self.validation.validPrayers(line): 
                    self.osrs.keyPress("F6")
                
                elif self.validation.validSpells(line): 
                    self.osrs.keyPress("F7")

                elif self.validation.validLogout(line):
                    self.osrs.keyPress("F9")
                    self.osrs.logout()
                    time.sleep(2)
                    self.checkLoginScreen()

                elif self.validation.validGroup(line): 
                    self.osrs.keyPress("F10")

                elif self.validation.validEmotes(line): 
                    self.osrs.keyPress("F11")
                
                elif self.validation.validMusic(line):
                    self.osrs.keyPress("F12")

                #If the entire line is a number get the first number
                elif self.validation.validNumerical(line):
                    #GET THE FIRST DIGIT of the first line
                    firstNum = re.split("[^\d]", line)[0][0]
                    print(firstNum)
                    if(int(firstNum)):
                        self.osrs.keyPress(firstNum)

                elif secondNum:
                    #move mouse x y
                    if self.validation.validMouseMoveTo(line):
                        dur = line.split(' ')
                        self.win.moveMouse((num, secondNum))
                    
                    
                    #move mouse x y
                    elif self.validation.validMouseMove(line):
                        dur = line.split(' ')
                        self.win.moveMouseRelative((num, secondNum * -1))
                    
                    else:
                        wasValidLine = False

                else:
                    wasValidLine = False
        else:
            wasValidLine = False
        return wasValidLine
from pickletools import pyunicode
import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
from config import *


class osrsController:

    def __init__(self, win):

        self.inv = self.invGrid(win)
        self.main = self.mainGrid(win)
        self.map = self.mapGrid(win)
        self.buttons = self.uiButtons()
        self.bank = self.bankButtons()
        self.win = win


    class mainGrid:
        def __init__(self, win):
            self.win = win
            self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
            self.rows = range(1,14)
            self.StartX = 20
            self.StartY = 40
            self.SqWidth = 25.5
            self.SqHeight = 25.5
            self.endX = self.StartX + (self.SqWidth * len(self.cols))
            self.endY = self.StartY + (self.SqHeight * len(self.rows))
            self.centerX = self.StartX + ((self.endX - self.StartX) / 2)
            self.centerY = self.StartY + ((self.endY - self.StartY) / 2)

        def checkCoord(self, letter, num):
            return letter in self.cols and num in self.rows

        # Get coords for some pos in main screen grid
        def pos(self,letter,num):
            xCoord = self.StartX + (self.cols.index(letter) * self.SqWidth)
            yCoord = self.StartY + ((num-1) * self.SqHeight)
            return xCoord, yCoord


        def clickPos(self, letter, number, right=False):
            self.win.moveMouse(self.pos(letter,number))
            if right: 
                pyautogui.click(button="right")
            else: 
                time.sleep(0.25)
                pyautogui.click()


        def move_dir(self, dir, num = 1):

            x = self.centerX
            y = self.centerY

            if dir in ['left','right','up','down'] and num < 7 and num > 0:
                if dir == 'left':
                    x = self.centerX - (self.SqWidth * num) - 10
                elif dir == 'right':
                    x = self.centerX + (self.SqWidth * num)
                elif dir == 'up':
                    y = self.centerY - (self.SqHeight * num)
                elif dir == 'down':
                    y = self.centerY + (self.SqHeight * (num)) + 15

                self.win.moveMouse([x,y])
                pyautogui.click()


    
    class invGrid:
        def __init__(self, win):
            self.win = win
            self.cols = ['w','x','y','z']
            self.rows = range(1,8)
            self.StartX = 575
            self.StartY = 250
            self.SqWidth = 45
            self.SqHeight = 37

        def checkCoord(self, letter, num):
            return letter in self.cols and num in self.rows

        ## Get Coords for some position in inventory grid
        def pos(self, letter, number):
            xCoord = self.StartX + (self.cols.index(letter) * self.SqWidth)
            yCoord = self.StartY + ((number-1) * self.SqHeight)
            return xCoord, yCoord


        def clickPos(self, letter, number, right=False):
            self.win.moveMouse(self.pos(letter,number))
            if right:     
                pyautogui.click(button="right")
            else:
                time.sleep(0.25)
                pyautogui.click()


        def dropItem(self, letter, number):
            self.win.moveMouse(self.pos(letter,number))
            pyautogui.keyDown("shift")
            time.sleep(0.05)
            pyautogui.click()
            time.sleep(0.05)
            pyautogui.keyUp("shift")


        def dragItem(self, l1, n1, l2, n2):
            self.win.moveMouse(self.pos(l1,n1))
            pyautogui.mouseDown()
            time.sleep(0.05)
            self.win.moveMouse(self.pos(l2,n2))
            time.sleep(0.05)
            pyautogui.mouseUp()



    class mapGrid:
        def __init__(self,win):
            self.win = win

            self.xCenter = 646
            self.yCenter = 111
            self.rad = 70
            self.dirs = {'ul':(-1,-1), 'u':(0,-1),'ur':(1,-1),'r':(1,0),'dr':(1,1),'d':(0,1),'dl':(-1,1),'l':(-1,0)}
            
            
            ## Maybe unnecessary, always calculable
            self.leftEdge = (576,111)
            self.topEdge = (645, 36)
            self.bottomEdge = (646, 185)
            self.rightEdge = (718, 111)

            

        def clickMap(self, dir, dist = 80):
            print('clicking')
            clickdirs = self.dirs[dir]
            xdir = clickdirs[0]
            ydir = clickdirs[1]

            xdist = self.rad * dist * xdir / 100
            ydist = self.rad * dist * ydir / 100

            xclick = self.xCenter + xdist 
            yclick = self.yCenter + ydist

            self.win.moveMouse((xclick,yclick))
            pyautogui.click()

            

        


        
    class uiButtons:
        def __init__(self):
            self.prayer = (560, 117) # TODO: Flags to know whether run is on or off
            self.run = (570, 150)
            self.sprintOn = False
            self.compass = (565, 48)
            self.special = (600, 175)
            self.logout = (650, 460)
            
            

        def clickCompass(self): 
            pyautogui.click(self.compass)

        def clickPrayer(self): 
            pyautogui.click(self.prayer)

        def clickRun(self): 
            pyautogui.click(self.run)

        def clickSpecial(self): 
            pyautogui.click(self.special)

        def clickLogout(self):
            pyautogui.click(self.logout)

        def checkRun(self, im=None):
            x = self.run[0]
            y = self.run[1]
            self.sprintOn = imagesearcharea("Images/run_on.PNG", x - 20, y - 20, x + 20, y + 20,  0.8)[0] != -1
            print(self.sprintOn)
            return self.sprintOn


    class bankButtons:
        def __init__(self):
            self.bankInv = (445, 340)
            self.bankEquip = (485, 340)
            self.quantities = self.bankQuantities()
            self.pin = 6934

        class bankQuantities:
            def __init__(self):
                self.q1 = (240, 350)
                self.q5 = (262, 350)
                self.q10 = (285, 350)
                self.qX = (312, 350)
                self.qAll = (340, 350)

        def depositInv(self):
            pyautogui.click(self.bankInv)


        def depositEquip(self):
            pyautogui.click(self.bankEquip)


        def changeQuantity(self, which):
            if which == '1':
                pyautogui.click(self.quantities.q1)
            elif which == '5':
                pyautogui.click(self.quantities.q5)
            elif which == '10':
                pyautogui.click(self.quantities.q10)
            elif which == 'x':
                pyautogui.click(self.quantities.qX)
            elif which == 'all':
                pyautogui.click(self.quantities.qAll)

        def openBank(self, keyPress, pin):
            for char in pin:
                keyPress(char)


    def openBank(self, pin):
        self.bank.openBank(self.keyPress,pin)


    # click some number of menu items below current pos
    def menuClick(self, num):
        self.win.moveMouseRelative((0, 20))
        self.win.moveMouseRelative((0, 15.8*(num-1)))
        pyautogui.click()
        
    
    def typeText(self, line, enter = False):
        text = " ".join(line.split(" ")[1:][0:100])
        print(text)
        pyautogui.write(text, interval=0.1)
        if enter:
            self.pressEnter()


    def pressEnter(self):
        pyautogui.keyDown("Enter")
        time.sleep(0.1) 
        pyautogui.keyUp("Enter")
 
        
    def keyPress(self, key, sleepTimer=100):
        pyautogui.keyDown(key)
        time.sleep(sleepTimer/1000)
        pyautogui.keyUp(key)


    def arrowKey(self, key, sleepTimer=250):
        pyautogui.keyDown(key)
        time.sleep(sleepTimer/1000)
        pyautogui.keyUp(key)
    
    def repeatPress(self, key, timeframe, presses=10):
        for i in range(0, presses):
            self.keyPress(key, 50)
            time.sleep((timeframe/1000)/presses)
        pass


    def zoom(self, dir, tick=500):
        if dir=="up" or dir=="in":
            pyautogui.scroll(tick)
            print(tick)
        elif dir=="down" or dir=="out":
            pyautogui.scroll(-tick)


    def logout(self):
        self.buttons.clickLogout()


    def login(self):
        isOnDC = imagesearcharea("Images/disconnectscreen.PNG", *self.win.screenshot.region(), 0.8)
        if isOnDC[0] != -1:
            self.win.moveMouse((430, 320))
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
        self.win.moveMouse((430, 320))
        time.sleep(0.25)
        pyautogui.click()
    

    def calibration(self):
        for i in range(len(self.main.cols)):
            for j in range(len(self.main.rows)):
                self.moveMouse((self.main.StartX + self.main.SqWidth*i, self.main.StartY + self.main.SqHeight*j))
                time.sleep(0.001)
        
        self.moveMouse((self.inv.StartX,self.inv.StartY))
        for i in range(0, 4):
            for j in range(0, 7):
                self.moveMouse((self.inv.StartX + self.inv.SqWidth*i, self.inv.StartY + self.inv.SqHeight*j))
                time.sleep(0.01)








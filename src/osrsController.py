import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
from config import *


class osrsController:

    def __init__(self, win):

        self.inv = self.invGrid()
        self.main = self.mainGrid()
        self.buttons = self.uiButtons()
        self.win = win


    class mainGrid:
        def __init__(self):
            self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
            self.rows = range(1,14)
            self.StartX = 20
            self.StartY = 40
            self.SqWidth = 25.5
            self.SqHeight = 25.5

    class invGrid:
        def __init__(self):
            self.cols = ['w','x','y','z']
            self.rows = range(1,8)
            self.StartX = 575
            self.StartY = 250
            self.SqWidth = 45
            self.SqHeight = 37

    class uiButtons:
        def __init__(self):
            self.prayer = (560, 117) # TODO: Flags to know whether run is on or off
            self.run = (560, 117)
            self.compass = (565, 48)
            self.special = (600, 175)

        def clickCompass(self): 
            pyautogui.click(self.compass)

        def clickPrayer(self): 
            pyautogui.click(self.prayer)

        def clickRun(self): 
            pyautogui.click(self.run)

        def clickSpecial(self): 
            pyautogui.click(self.special)


    # click some number of menu items below current pos
    def menuClick(self, num):
        self.win.moveMouseRelative(0, 20)
        self.win.moveMouseRelative(0, 15.8*(num-1))
        pyautogui.click()

    ## Get Coords for some position in inventory grid
    def inv_pos(self, letter, number):
        xCoord = self.inv.StartX + (self.inv.cols.index(letter) * self.inv.SqWidth)
        yCoord = self.inv.StartY + ((number-1) * self.inv.SqHeight)
        return xCoord, yCoord

    # Get coords for some pos in main screen grid
    def main_pos(self,letter,num):
        xCoord = self.main.StartX + (self.main.cols.index(letter) * self.main.SqWidth)
        yCoord = self.main.StartY + ((num-1) * self.main.SqHeight)
        return xCoord, yCoord


    def clickMain(self, letter, number, right=False):
        self.win.moveMouse(self.main_pos(letter,number))
        if right: 
            pyautogui.click(button="right")
        else: 
            time.sleep(0.25)
            pyautogui.click()

    def clickInv(self, letter, number, right=False):
        self.win.moveMouse(self.inv_pos(letter,number))
        if right:     
            pyautogui.click(button="right")
        else:
            time.sleep(0.25)
            pyautogui.click()
    
    def typeText(self, line):
        pyautogui.write(line.split("say: ")[1][0:40], interval=0.1)
        pyautogui.keyDown("Enter")
        time.sleep(0.1) 
        pyautogui.keyUp("Enter")

    def dropItem(self, letter, number):
        self.win.moveMouse(self.inv_pos(letter,number))
        pyautogui.keyDown("shift")
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.keyUp("shift")
    
    def dragItem(self, l1, n1, l2, n2):
        self.win.moveMouse(self.inv_pos(l1,n1))
        time.sleep(0.1)
        tupleCoords = self.inv_pos(l2,n2)
        pyautogui.dragTo(tupleCoords[0], tupleCoords[1], duration=0.1)

    def checkMainCoord(self, letter, num):
        return letter in self.main.cols and num in self.main.rows

    def checkInvCoord(self, letter, num):
        return letter in self.inv.cols and num in self.inv.rows

    def login(self):
        isOnMainScreen = imagesearch("Images/loginscreen.PNG", 0.8)
        if isOnMainScreen[0] != -1:
            isOnDC = imagesearch("Images/disconnectscreen.PNG", 0.8)
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
    
    def arrowKey(self, key, sleepTimer=250):
        pyautogui.keyDown(key)
        time.sleep(sleepTimer/1000)
        pyautogui.keyUp(key)

    def zoom(self, dir, tick=500):
        if dir=="up" or dir=="in":
            pyautogui.scroll(tick)
            print(tick)
        elif dir=="down" or dir=="out":
            pyautogui.scroll(-tick)

    def keyPress(self, key, sleepTimer=100):
        pyautogui.keyDown(key)
        time.sleep(sleepTimer/1000)
        pyautogui.keyUp(key)

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








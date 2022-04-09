import socket, time
from tkinter.tix import MAX
from imagesearch import *
import pyautogui
import re
from config import *


class osrsController:

    class mainGrid:
        def __init__(self):
            self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']
            self.StartX = 20
            self.StartY = 40
            self.SqWidth = 25.5
            self.SqHeight = 25.5

    class invGrid:
        def __init__(self):
            self.cols = ['w','x','y','z']
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

    class winSize:
        xMax = 760
        yMax = 480
        xMin = 0 
        yMin = 25

        def check_x(self,x):
            return x < self.xMax and x > self.xMin

        def check_y(self,y):
            return y < self.yMax and y > self.yMin



    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.nickname = 'newtwitchplaysosrs'

        self.inv = self.invGrid()
        self.main = self.mainGrid()
        self.buttons = self.uiButtons()
        self.win = self.winSize()

        self.sock = socket.socket()
 

    # Return mouse positions
    def mouse_x_pos(self):
        return pyautogui.position()[0]

    def mouse_y_pos(self):
        return pyautogui.position()[1]
    

    # Mouse moving functions, one absolute the other relative to curr pos
    def moveMouse(self, x, y):
        if self.win.check_x(x) and self.win.check_y(y):
            pyautogui.moveTo(x, y)

    def moveMouseRelative(self, x, y):
        if self.win.check_x(x + self.mouse_x_pos()) and self.win.check_y(y + self.mouse_y_pos()):
            pyautogui.move(x, y)



    ## Get Coords for some position in inventory grid
    def inv_pos(self, letter, number):
        xCoord = self.inv.StartX + (self.inv.cols.index(letter) * self.inv.SqWidth)
        yCoord = self.inv.StartY + ((number-1) * self.inv.SqHeight)
        return xCoord, yCoord

    # Get coords for some pos in main screen grid
    def main_pos(self,letter,num):
        xCoord = self.main.StartX + (self.main.cols.index(letter) * self.main.SqWidth)
        yCoord = self.main.StartY + ((num-1) * self.main.SqHeight)


    def clickMain(self, letter, number, right=False):
        moveMouse(self.main_pos(letter,number))
        if right: 
            pyautogui.click(button="right")
        else: 
            time.sleep(0.25)
            pyautogui.click()

    def clickInv(self, letter, number, right=False):
        moveMouse(self.inv_pos(letter,number))
        if right:     
            pyautogui.click(button="right")
        else:
            time.sleep(0.25)
            pyautogui.click()

    def dropItem(self, letter, number):
        moveMouse(self.inv_pos(letter,number))
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





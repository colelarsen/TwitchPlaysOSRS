from ttvController import TtvController
import ttvController as ttv
import socket, time
import pyautogui


ttvCont = ttv.TtvController()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        ttvCont.parseChat("bank open 4183")
        time.sleep(.5)
        

    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

#while True:
#    print(pyautogui.position())
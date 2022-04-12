from ttvController import TtvController
import ttvController as ttv
import socket, time
import pyautogui


ttvCont = ttv.TtvController()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        ttvCont.parseChat("bank q1")
        time.sleep(1)
        ttvCont.parseChat("bank q5")
        time.sleep(1)
        ttvCont.parseChat("bank q10")
        time.sleep(1)
        ttvCont.parseChat("bank qx")
        time.sleep(1)
        ttvCont.parseChat("bank qall")
    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

#while True:
#    print(pyautogui.position())
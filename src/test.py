from ttvController import TtvController
import ttvController as ttv
import socket, time
import pyautogui


def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        time.sleep(4)
        ttvCont.parseChat("login")
        time.sleep(5)
        ttvCont.parseChat("logout 5724")
        time.sleep(5)
        ttvCont.parseChat("login")
        time.sleep(5)


        

    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

# while True:
#    print(pyautogui.position())
from ttvController import TtvController
import ttvController as ttv
import socket, time
import pyautogui


ttvCont = ttv.TtvController()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        ttvCont.readChatTwitch("a" + '\r\n' + "b" + '\r\n' + "c" + '\r\n')

    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

#while True:
#    print(pyautogui.position())
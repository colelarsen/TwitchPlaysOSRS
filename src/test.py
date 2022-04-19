from ttvController import TtvController
import ttvController as ttv
import messageHandler
import socket, time
import pyautogui


def testSingle(): 
    ttvCont = ttv.TtvController()
    messageHandlerC = messageHandler.messageHandler("testOutput.txt")
    try:
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message("ttv", "tester", "drop w1"))
    except Exception as e: 
        print(e)

        
testSingle()

# while True:
#    print(pyautogui.position())
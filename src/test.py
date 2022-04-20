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
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"login"))
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"mouse 300 150"))
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"j7 15askf ???"))
    except Exception as e: 
        print(e)

        
testSingle()

# while True:
#    print(pyautogui.position())
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
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"m dr 100"))
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"m dl 90"))
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"m ur 95"))
        time.sleep(4)
        ttvCont.parseChat(messageHandlerC.message('testSrc','testAuthor',"m ul 90"))
        time.sleep(4)
        

    except Exception as e: 
        print(e)

        
testSingle()

# while True:
#     print(pyautogui.position())
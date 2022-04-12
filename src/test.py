import ttvController as ttv
import socket, time
import pyautogui


ttvCont = ttv.TtvController()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        ttvCont.parseChat("drag x1 z1")
    except Exception as e: 
        print(e)
    time.sleep(2)
    try:
        ttvCont.parseChat("drag w7 x3")
    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

#while True:
#    print(pyautogui.position())
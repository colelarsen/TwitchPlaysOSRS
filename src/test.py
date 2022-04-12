from ttvController import TtvController
import ttvController as ttv
import socket, time
import pyautogui


ttvCont = ttv.TtvController()

def testSingle(): 
    ttvCont = ttv.TtvController()
    try:
        #ttvCont.parseChat("rw1")
        #time.sleep(1)
        #ttvCont.parseChat("w1")
        #time.sleep(1)
        #ttvCont.parseChat("j7")
        #time.sleep(1)
        #ttvCont.parseChat("rj7")
        time.sleep(1)
        ttvCont.parseChat("zoom in 400")
        time.sleep(1)
        ttvCont.parseChat("scroll out 3m")
        time.sleep(3)
        ttvCont.parseChat("scroll in")
        
    except Exception as e: 
        print(e)

        
time.sleep(4)
testSingle()

#while True:
#    print(pyautogui.position())
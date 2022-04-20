import re
import osrsController as osrs
import utility


## Organized these by general area they are working with. Worth considering putting these into objects for mouse, keyboard, main, inventory, hud, inventoryhud

class ValidationController:
    def __init__(self, osrs, win):
        self.osrs = osrs
        self.win = win
    
    # What this does
    def isValidInput(self, line):
        public_method_names = [method for method in dir(self) if callable(getattr(self, method)) if not method.startswith('_') if not method.startswith("isValidInput")]  # 'private' methods start from _
        for method in public_method_names:
            if getattr(self, method)(line):
                return True
        return False
        

    ######################### MOUSE VALIDATION #########################

    def validClick(self, line):
        return line in ["c", "lc", "click", "left click", "lclick"]


    def validRClick(self, line):
        return line in ["r", "rc", "right click", "r click", "rclick"]


    def validMouseMoveTo(self, line): ## I think we should change this to be "mouse x y"
        if line.startswith("mouse to"):
            dur = line.split(' ')
            return len(dur) == 5 and (int(dur[2]) <= self.win.xMax and int(dur[3])*-1 <= self.win.yMax)
        return False
    
    def validMouseMove(self, line): ## and change this to be "mouserel x y" or smth, not as sold on this. we could also do like "mouse [dir] [num]"
        if line.startswith("mouse "):
            dur = line.split(' ')
            return len(dur) == 4 and (int(dur[1]) <= self.win.xMax and int(dur[2])*-1 <= self.win.yMax)
        return False
    
    def validCenterMouse(self, line):
        return line.startswith("center mouse")
    
    def validMenu(self, line):
        if re.match("^(m|menu) [0-9]( +.*)?$", line):
            return True
        return False
    
    def validZoom(self, line): # Identical, merge
        if re.match("^(zoom) (in|out)( [1-5]?( +.*)?)?",line):
            self.win.moveMouse((260, 210))
            return line
        return False
    
    def validScroll(self, line):
        if re.match("^(scroll) (in|out|down|up)( [1-5]?( +.*)?)?",line):
            return line
        return False
        #return line=="scroll up"or line=="scroll down"

    #####################################################################
    


    ######################### KEYPRESS VALIDATIONS #########################

    def validEscape(self, line):
        return line in ["escape", "cancel", "quit", "exit", "esc"]

    def validSay(self, line):
        if(re.match("^say: ((?!::).)*$", line)):
            return True
        return False

    def validType(self,line):
        if(re.match("^type: ((?!::).)*$", line)):
            return True
        return False
    
    def validCam(self, line):
        if line.startswith("cam ") or line.startswith("c "):
            lineWords = line.split(' ')
            dir = lineWords[1]
            if len(lineWords) == 3 and dir in ["left", "right", "down", "up"]:
                num = utility.getFirstNumber(line)
                return num <= 5000
            if dir in ["left", "right", "down", "up"]:
                return True
        return False

    def validAngleCam(self,line):
        if line.startswith("cam ") or line.startswith("c "):
            lineWords = line.split(' ')
            dir = lineWords[1]
            if dir in ['qtr','qtl']:
                return True
        return False

    def validSpace(self, line):
        if re.match("^((spacebar)|(space)|(sp))( [0-9]+)?( +.*)?$", line):
            return True
        return False

    def validNumerical(self, line):
        return line.isnumeric()

    #########################################################################



    ######################### MAIN WINDOW VALIDATION #########################

    def validMainLClick(self, line):
        if re.match("^([a-t][1-9][0-3]?)( +.*)?$", line):
            letter = line[0]
            num = utility.getFirstNumber(line)
            return self.osrs.main.checkCoord(letter, num)
        return False
    
    def validMainRClick(self, line):
        if re.match("^(r[a-t][1-9][0-3]?)( +.*)?$", line):
            letter = line[1]
            num = utility.getFirstNumber(line)
            return self.osrs.main.checkCoord(letter, num)
        return False

    def validStop(self, line):
        return line=="stop"
    
    def validBankOpen(self,line):
        if re.match("^(bank open)( [\d]{4}( +.*)?)?$",line):
            return True
        return False

    def validBankDeposit(self,line):
        if re.match("^((bank ))((inv|inventory|equipment|equip)( +.*)?)?$",line):
            return True
        return False

    def validBankQuantity(self,line):
        if re.match("^((bank ))((q1|q5|q10|qx|qall)( +.*)?)+",line):
            return True
        return False

    def validDir(self,line):
        if re.match("^((left)|(right)|(down)|(up)|(u)|(d)|(l)|(r))(( [1-7])( +[^1-7].*)?)?$", line):
           return True
        return False 

    ###########################################################################



    ######################### INVENTORY VALIDATION #########################

    def validInvLClick(self, line):
        if re.match("^([w-z][1-9][0-3]?)( +.*)?$", line):
            num = utility.getFirstNumber(line)
            return self.osrs.inv.checkCoord(line[0], num)
        return False


    def validInvRClick(self, line):
        if re.match("^(r[w-z][1-9])( +.*)?$", line):
            num = utility.getFirstNumber(line)
            return self.osrs.inv.checkCoord(line[1], num)
        return False


    def validDrag(self, line):
        if re.match("^drag ?([w-z][1-9]) ?([w-z][1-9])( +.*)?$", line):
            lineWords = line.split(' ')
            firstBar = lineWords[1]
            secondBar = lineWords[2]
            num1 = utility.getFirstNumber(firstBar)
            num2 = utility.getFirstNumber(secondBar)
            return self.osrs.inv.checkCoord(firstBar[0], num1) and self.osrs.inv.checkCoord(secondBar[0], num2)
        return False
    
    
    def validDrop(self, line):
        #perform left click on coordinates given
        if re.match("^(drop [w-z][1-7])( +.*)?$", line): 
            coords = line.split(' ')[1].strip()
            num = utility.getFirstNumber(coords)
            return self.osrs.inv.checkCoord(coords[0], num)
        if re.match("^(d[ ]?[w-z][1-7])( +.*)?$", line): 
            coords = line.split('d')[1].strip()
            if coords.startswith(' '):
                coords = line.split(' ')[1].strip()
            num = utility.getFirstNumber(coords)
            return self.osrs.inv.checkCoord(coords[0], num)
        return False

    def validQuickUse(self, line):
        if re.match("^(qu)( [w-z][1-7])?", line):
            return line
        return False

    ########################################################################



    ######################### HUD VALIDATIONS #########################

    def validMapMove(self, line):
        if re.match("^((map)|(mm)|(m) ((tr)|(ur)|(br)|(bl)|(ul)|(tl)|(bottom)|(top)|(up)|(bot)|(down)|(left)|(right)|(t)|(b)|(d)|(u)|(l)|(r)))( +.*)?$", line): 
            return True
        return False
    
    def validResetCam(self, line):
        return line in ["reset", "reset camera", "compass"]
    
    def validRun(self, line):
        return line in ["run", "walk", "sprint"]
    
    def validSpecialAttack(self, line):
        return line in line in ["sa", "special", "special attack"]
    
    def validPrayer(self, line):
        return line in ["pray", "prayer"]
    
    ####################################################################

    

    ######################### INVENTORY HUD BUTTON VALIDATION #########################
    
    def validCombat(self, line):
        return  line == "combat" or line == "style" or line == "attack style"
    
    def validStats(self, line):
        return  line == "stats" or line == "exp"
    
    def validGroup(self, line):
        return  line == "chat channel" or line == "minigame" or line == "clan" or line == "group"
    
    def validQuests(self, line):
        return  line in ["quests", 'quest']
    
    def validInv(self, line):
        return line == "i" or line == "inv" or line == "inventory"
    
    def validLogin(self, line):
        return line == "login"

    def validLogout(self,line):
        return line == "logout 5724"
    
    def validGear(self, line):
        return   line == "gear" or line == "equip" or line == "equipment"
    
    def validPrayers(self, line):
        return line == "prayers"
    
    def validSpells(self, line):
        return line == "spells" or line == "spellbook"
    
    def validEmotes(self, line):
        return  line == "emote" or line == "emotes"
    
    def validMusic(self, line):
        return line == "music" or line == "song" or line =="songs"
    
    ######################################################################################


    
    
import re
import osrsController as osrs
import utility

class ValidationController:
    def __init__(self, osrs, win):
        self.osrs = osrs
        self.win = win
    
    def isValidInput(self, line):
        public_method_names = [method for method in dir(self) if callable(getattr(self, method)) if not method.startswith('_') if not method.startswith("isValidInput")]  # 'private' methods start from _
        for method in public_method_names:
            if getattr(self, method)(line):
                return True
        return False
        


    def validInvLClick(self, line):
        if re.match("^([w-z][1-9][0-3]?)( +.*)?$", line):
            num = utility.getFirstNumber(line)
            return self.osrs.checkInvCoord(line[0], num)
        return False
    
    def validInvRClick(self, line):
        if re.match("^(r[w-z][1-9])( +.*)?$", line):
            num = utility.getFirstNumber(line)
            return self.osrs.checkInvCoord(line[1], num)
        return False
    
    def validDrag(self, line):
        if re.match("^drag ?([w-z][1-9]) ?([w-z][1-9])( +.*)?$", line):
            lineWords = line.split(' ')
            firstBar = lineWords[1]
            secondBar = lineWords[2]
            num1 = utility.getFirstNumber(firstBar)
            num2 = utility.getFirstNumber(secondBar)
            return self.osrs.checkInvCoord(firstBar[0], num1) and self.osrs.checkInvCoord(secondBar[0], num2)
        return False
    
    def validMainLClick(self, line):
        if re.match("^([a-t][1-9][0-3]?)( +.*)?$", line):
            letter = line[0]
            num = utility.getFirstNumber(line)
            return self.osrs.checkMainCoord(letter, num)
        return False
    
    def validMainRClick(self, line):
        if re.match("^(r[a-t][1-9][0-3]?)( +.*)?$", line):
            letter = line[1]
            num = utility.getFirstNumber(line)
            return self.osrs.checkMainCoord(letter, num)
        return False
    
    def validDrop(self, line):
        #perform left click on coordinates given
        if re.match("^(drop [w-z][1-7])( +.*)?$", line): 
            coords = line.split(' ')[1].strip()
            num = utility.getFirstNumber(coords)
            return self.osrs.checkInvCoord(coords[0], num)
        return False
    
    def validMapMove(self, line):
        if re.match("^([map, m, mm] ((tr)|(ur)|(br)|(bl)|(ul)|(tl)|(bottom)|(top)|(bot)|(down)|(left)|(right)|(t)|(b)|(d)|(l)|(r)))( +.*)?$", line): 
            return True
        return False
    
    def validEscape(self, line):
        return line in ["escape", "cancel", "quit", "exit"]
    
    def validQuickUse(self, line):
        return "qu"==line or line.startswith("qu ")
    
    def validClick(self, line):
        return line in ["c", "lc", "click", "left click", "lclick"]
    
    def validRClick(self, line):
        return line in ["r", "rc", "right click", "r click", "rclick"]
    
    def validStop(self, line):
        return line=="stop"
    
    def validResetCam(self, line):
        return line in ["reset", "reset camera", "compass"]
    
    def validRun(self, line):
        return line in ["run", "walk", "sprint"]
    
    def validSpecialAttack(self, line):
        return line in line in ["sa", "special", "special attack"]
    
    def validPrayer(self, line):
        return line in ["pray", "prayer"]
    
    def validSay(self, line):
        if(re.match("^say: ((?!::).)*$", line)):
            return True
        return False
    
    def validCam(self, line):
        if line.startswith("cam ") or line.startswith("c "):
            lineWords = line.split(' ')
            dir = lineWords[1]
            if len(lineWords) == 3 and dir in ["left", "right", "down", "up"]:
                num = utility.getFirstNumber(line)
                return num <= 3000
            if dir in ["left", "right", "down", "up"]:
                return True
        return False
    
    def validMouseMoveTo(self, line):
        if line.startswith("move mouse to"):
            dur = line.split(' ')
            return len(dur) == 5 and (int(dur[3]) <= self.win.xMax and int(dur[4])*-1 <= self.win.yMax)
        return False
    
    def validMouseMove(self, line):
        if line.startswith("move mouse "):
            dur = line.split(' ')
            return len(dur) == 4 and (int(dur[2]) <= self.win.xMax and int(dur[3])*-1 <= self.win.yMax)
        return False
    
    def validCenterMouse(self, line):
        return line.startswith("center mouse")
    
    def validMenu(self, line):
        if re.match("^(m|menu) [0-9]( +.*)?$", line):
            return True
        return False
    
    def validZoom(self, line):
        return line=="zoom in" or line=="zoom out"
    
    def validScroll(self, line):
        return line=="scroll up"or line=="scroll down"
    
    def validSpace(self, line):
        if re.match("^((spacebar)|(space))( [0-9]+)?( +.*)?$", line):
            return True
        return False
    
    def validCombat(self, line):
        return  line == "combat" or line == "style" or line == "attack style"
    
    def validStats(self, line):
        return  line == "stats" or line == "exp"
    
    def validGroup(self, line):
        return  line == "chat channel" or line == "minigame" or line == "clan" or line == "group"
    
    def validQuests(self, line):
        return  line == "quests"
    
    def validInv(self, line):
        return line == "i" or line == "inv" or line == "inventory"
    
    def validLogin(self, line):
        return line == "login"
    
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
    
    def validNumerical(self, line):
        return line.isnumeric()
    
    
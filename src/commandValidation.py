import re
import osrsController as osrs
import utility

class ValidationController:
    def __init__(self, osrs):
        self.osrs = osrs

    def validInvLClick(self, line):
        if re.match("[w-z][1-7][^0-9]?.*", line):
            num = utility.getFirstNumber(line)
            return self.osrs.checkInvCoord(line[0], num)
        return False
    
    def validInvRClick(self, line):
        print(line)
        if re.match("r[w-z][1-7][^0-9]?.*", line):
            num = utility.getFirstNumber(line)
            return self.osrs.checkInvCoord(line[1], num)
        return False
    
    def validMainLClick(self, line):
        if re.match("[a-t][1-9][0-3]?.*", line):
            letter = line[0]
            num = utility.getFirstNumber(line)
            return self.osrs.checkMainCoord(letter, num)
        return False
    
    def validMainRClick(self, line):
        if re.match("r[a-t][1-9][0-3]?.*", line):
            letter = line[1]
            num = utility.getFirstNumber(line)
            return self.osrs.checkMainCoord(letter, num)
        return False
    
    def validDrop(self, line):
        #perform left click on coordinates given
        if re.match("drop [w-z][1-7][^0-9]?.*", line): 
            coords = line.split(' ')[1].strip()
            num = utility.getFirstNumber(coords)
            return self.osrs.checkInvCoord(coords[0], num)
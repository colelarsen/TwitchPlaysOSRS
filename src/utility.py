import re
def getFirstNumber(line):
    number = re.search(r"[\d]+", line)
    if number:
        number = int(line[number.start():number.end()])
    return number

def getSecondNumber(line):
    number = re.search(r"[\d]+ [\d]+", line)
    if number:
        nums = line[number.start():number.end()]
        number = int(nums.split(' ')[1])
    return number